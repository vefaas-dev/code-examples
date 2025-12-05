// Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

package es

import (
	"bytes"
	"crypto/tls"
	"encoding/base64"
	"encoding/json"
	"fmt"
	"net/http"
	"time"
)

type Conf struct {
	// ES实例的内网或公网访问地址，可在实例信息页面获取
	Host string `json:"host"`
	// 登录实例的访问用名，默认为 admin
	Username string `json:"username"`
	// 登录实例用户名的密码
	Password string `json:"password"`
	// ES索引名称，需要提前创建好
	Index string `json:"index"`
}

type Client struct {
	httpClient *http.Client
	conf       *Conf
}

var client *Client

func InitESClient(conf *Conf) {
	client = &Client{
		httpClient: &http.Client{
			Timeout: 5 * time.Second,
			Transport: &http.Transport{
				TLSClientConfig: &tls.Config{InsecureSkipVerify: true},
			},
		},
		conf: conf,
	}
}

func CreateESDocument(document interface{}) error {
	url := fmt.Sprintf("%s/%s/_doc", client.conf.Host, client.conf.Index)
	reqBody, err := json.Marshal(document)
	if err != nil {
		errMsg := fmt.Sprintf("marshal request body error %v", err)
		return fmt.Errorf(errMsg)
	}
	request, err := http.NewRequest(http.MethodPost, url, bytes.NewReader(reqBody))
	if err != nil {
		return err
	}
	request.Header.Set("Content-Type", "application/json")
	request.Header.Set("Authorization", generateBasicAuth(client.conf.Username, client.conf.Password))

	resp, err := client.httpClient.Do(request)
	if err != nil {
		return err
	}
	if resp.StatusCode != http.StatusOK && resp.StatusCode != http.StatusCreated {
		return fmt.Errorf("return non 200 http code: %d", resp.StatusCode)
	}
	return nil
}

func generateBasicAuth(username, password string) string {
	auth := username + ":" + password
	return "Basic " + base64.StdEncoding.EncodeToString([]byte(auth))
}

func (conf *Conf) Validate() error {
	if conf.Host == "" || conf.Username == "" || conf.Password == "" || conf.Index == "" {
		return fmt.Errorf("must specify host, username, password and index")
	}
	return nil
}
