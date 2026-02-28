import { createTool } from '@mastra/core/tools';
import { z } from 'zod';
import { SandboxService } from '../sandbox/sandbox-service';

const svc = () => SandboxService.getInstance();

export const sandboxFileOperations = createTool({
  id: 'sandbox_file_operations',
  description: `Unified file system operations tool. /tmp and /home/gem are fully accessible. Default working directory is /home/gem.

Actions:
- read: Read file content. Uses "file" path. Optional start_line/end_line (0-based).
- write: Write content to file. Uses "file" path. Optional append/encoding.
- replace: Replace a string in file. Uses "file" path, requires old_str and new_str.
- list: List directory contents. Optional recursive/show_hidden/file_types.
- find: Find files by name pattern (glob syntax). Requires glob pattern.
- grep: Search file content with regex across files. Optional include/exclude/case_insensitive/context_before/context_after.
- glob: Enhanced glob matching with metadata.`,
  inputSchema: z.object({
    action: z.enum(['read', 'write', 'replace', 'list', 'find', 'grep', 'glob'])
      .describe('Operation type'),
    path: z.string()
      .describe('File path (for read/write/replace) or directory path (for list/find/grep/glob). Default to /home/gem'),
    content: z.string().optional()
      .describe('Content to write (required for write)'),
    old_str: z.string().optional()
      .describe('Original string to replace (required for replace)'),
    new_str: z.string().optional()
      .describe('New string to replace with (required for replace)'),
    pattern: z.string().optional()
      .describe('Glob pattern for find, regex pattern for grep/glob'),
    encoding: z.enum(['utf-8', 'base64', 'raw']).optional()
      .describe('File encoding for write (default: utf-8)'),
    start_line: z.number().int().optional()
      .describe('Starting line for read, 0-based'),
    end_line: z.number().int().optional()
      .describe('Ending line for read, not included'),
    append: z.boolean().optional()
      .describe('Append mode for write (default: false)'),
    recursive: z.boolean().optional()
      .describe('Recursive mode for find/list/grep (default: false for list, true for grep)'),
    show_hidden: z.boolean().optional()
      .describe('Show hidden files in list (default: true)'),
    file_types: z.array(z.string()).optional()
      .describe('Filter by file extensions for list, e.g. [".py", ".ts"]'),
    include: z.array(z.string()).optional()
      .describe('File glob filters for grep, e.g. ["*.py", "*.ts"]'),
    exclude: z.array(z.string()).optional()
      .describe('Glob patterns to exclude for grep/glob, e.g. ["node_modules"]'),
    case_insensitive: z.boolean().optional()
      .describe('Case insensitive search for grep (default: false)'),
    fixed_strings: z.boolean().optional()
      .describe('Treat pattern as literal string for grep (default: false)'),
    context_before: z.number().int().optional()
      .describe('Lines before each match for grep (0-20, default: 0)'),
    context_after: z.number().int().optional()
      .describe('Lines after each match for grep (0-20, default: 0)'),
    max_results: z.number().int().optional()
      .describe('Maximum number of results for grep/glob (default: 500)'),
  }),
  execute: async (input) => {
    const { action, path, content, old_str, new_str, pattern, encoding,
      start_line, end_line, append, recursive, show_hidden, file_types,
      include, exclude, case_insensitive, fixed_strings,
      context_before, context_after, max_results } = input;

    switch (action) {
      case 'read':
        return svc().post('/v1/file/read', {
          file: path,
          ...(start_line !== undefined && { start_line }),
          ...(end_line !== undefined && { end_line }),
        });
      case 'write':
        return svc().post('/v1/file/write', {
          file: path, content,
          ...(encoding && { encoding }),
          ...(append !== undefined && { append }),
        });
      case 'replace':
        return svc().post('/v1/file/replace', { file: path, old_str, new_str });
      case 'list':
        return svc().post('/v1/file/list', {
          path,
          ...(recursive !== undefined && { recursive }),
          ...(show_hidden !== undefined && { show_hidden }),
          ...(file_types && { file_types }),
        });
      case 'find':
        return svc().post('/v1/file/find', { path, glob: pattern });
      case 'grep':
        return svc().post('/v1/file/grep', {
          path, pattern,
          ...(include && { include }),
          ...(exclude && { exclude }),
          ...(case_insensitive !== undefined && { case_insensitive }),
          ...(fixed_strings !== undefined && { fixed_strings }),
          ...(context_before !== undefined && { context_before }),
          ...(context_after !== undefined && { context_after }),
          ...(max_results !== undefined && { max_results }),
          ...(recursive !== undefined && { recursive }),
        });
      case 'glob':
        return svc().post('/v1/file/glob', {
          path, pattern,
          ...(exclude && { exclude }),
          ...(max_results !== undefined && { max_results }),
        });
    }
  },
});

export const sandboxGetPackages = createTool({
  id: 'sandbox_get_packages',
  description: 'Get installed packages in the sandbox. Returns python and/or nodejs packages.',
  inputSchema: z.object({
    language: z.enum(['python', 'nodejs']).optional()
      .describe('Language filter. Omit to return both python and nodejs packages.'),
  }),
  execute: async (input) => {
    if (input.language === 'python') return svc().get('/v1/sandbox/packages/python');
    if (input.language === 'nodejs') return svc().get('/v1/sandbox/packages/nodejs');
    const [python, nodejs] = await Promise.all([
      svc().get('/v1/sandbox/packages/python'),
      svc().get('/v1/sandbox/packages/nodejs'),
    ]);
    return { python, nodejs };
  },
});

export const sandboxExecuteBash = createTool({
  id: 'sandbox_execute_bash',
  description: `Execute a shell command in the sandbox. Sessions are managed automatically.

- Default working directory is /home/gem.
- For temporary code snippets (e.g. get current time, check OS info), use /tmp and clean up after.
- Use session_id to preserve state across calls (e.g. cd into a directory, then run commands).`,
  inputSchema: z.object({
    command: z.string()
      .describe('Shell command to execute'),
    cwd: z.string().optional()
      .describe('Working directory (absolute path). Defaults to /home/gem'),
    timeout: z.number().optional()
      .describe('Timeout in seconds (default: 30, max: 3600)'),
    session_id: z.string().optional()
      .describe('Session ID to preserve state across calls'),
    env: z.record(z.string()).optional()
      .describe('Additional environment variables'),
  }),
  execute: async (input) => {
    return svc().post('/v1/shell/exec', {
      command: input.command,
      ...(input.cwd && { cwd: input.cwd }),
      ...(input.timeout && { timeout: input.timeout }),
      ...(input.session_id && { session_id: input.session_id }),
      ...(input.env && { env: input.env }),
    });
  },
});

export const sandboxConvertToMarkdown = createTool({
  id: 'sandbox_convert_to_markdown',
  description: 'Convert a resource (PDF, Word, HTML, URL, etc.) to Markdown format.',
  inputSchema: z.object({
    uri: z.string()
      .describe('Resource URI. Supports http:, https:, file:, or data: schemes.'),
  }),
  execute: async (input) => {
    return svc().post('/v1/util/convert_to_markdown', { uri: input.uri });
  },
});
