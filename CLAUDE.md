CLAUDE.md — Zyntro Media AI

«Organization engineering standards for Claude Code and AI coding agents.
These instructions apply to repositories using the Zyntro Media AI stack. Repository-specific instructions may add constraints but must not weaken security requirements.»

1. Engineering Principles

- Prioritize correctness, security, maintainability, and reproducibility.
- Inspect the repository structure, package scripts, existing conventions, and related tests before changing code.
- Prefer minimal, focused changes over unrelated refactoring.
- Never claim that a command, test, deployment, or rerun succeeded without evidence.
- Explain assumptions, risks, and verification results.
- Do not expose secrets, personal data, access tokens, or sensitive log contents.

2. Stack and Runtime

- Frontend: Next.js 14+ using the App Router.
- Language: TypeScript with strict mode enabled.
- Backend and database: Supabase PostgreSQL with "@supabase/supabase-js" v2.
- AI inference: "groq-sdk"; use other providers only through approved provider modules.
- Styling: Tailwind CSS.
- Package manager: npm. Do not suggest yarn or pnpm.
- Runtime: Node.js 20 LTS unless the repository specifies a compatible, approved version.
- Prefer dependencies that work in Termux on Android without native binary requirements.

Use Server Components by default. Add ""use client"" only when browser APIs, interactive event handlers, or client-side hooks are required.

3. Repository Structure

Use the following structure for Next.js repositories where appropriate:

app/
  (routes)/
  actions/
  api/
components/
  ui/
  [feature]/
lib/
  supabase/
  groq/
  ai/
  config.ts
  logger.ts
  utils/
types/
tests/
.github/
  workflows/
  copilot-instructions.md

- Keep components below 200 lines where practical.
- Keep functions at or below 40 lines where practical.
- Co-locate feature-specific types and tests.
- Place server actions in "app/actions/" with the ""use server"" directive.
- Avoid creating new directories that conflict with the repository's existing architecture.

4. TypeScript Standards

- Export named types instead of default-exported types.
- Prefer "interface" for object shapes and "type" for unions and intersections.
- Never introduce "any" without an explicit, justified exception.
- Use Zod schemas for validating external input and derive types using "z.infer<typeof Schema>".
- Type Supabase query results explicitly.
- Handle errors before consuming query data.
- Avoid unsafe type assertions and implicit "any".

Example:

interface Video {
  id: string;
  title: string;
  status: string;
}

const { data, error } = await supabase
  .from("videos")
  .select("id, title, status")
  .returns<Video[]>();

if (error) {
  throw new Error("Unable to retrieve videos.");
}

const videos = data ?? [];

5. Supabase and Data Security

- Enable and validate Row Level Security (RLS) for every application table.
- Derive authorization from verified user identity and appropriate database policies.
- Never expose "SUPABASE_SERVICE_ROLE_KEY" to client-side code.
- Use server-side Supabase helpers appropriate to the installed SDK and Next.js version.
- Use PostgreSQL functions or RPC for multi-step operations that require transactional consistency.
- Use Supabase Storage for file uploads rather than storing binary files in database rows.
- Validate and authorize all external input.
- Never assume TypeScript types replace database authorization.

6. AI Provider Architecture

Route AI requests through "lib/groq/" or "lib/ai/[provider]/". Components must not call provider SDKs directly.

Maintain model identifiers centrally:

export const MODELS = {
  groq: {
    fast: "llama-3.1-8b-instant",
    smart: "llama-3.3-70b-versatile",
  },
  fal: {
    imageGen: "fal-ai/flux/schnell",
  },
} as const;

Verify model availability and provider documentation before adopting model identifiers in production.

- Explicitly configure token limits and temperature.
- Validate prompts and user inputs.
- Use a typed "Result<T, Error>" pattern or an equivalent repository convention.
- Apply timeouts and bounded retries only to operations that are safe to repeat.
- Log provider, model, latency, and token usage without logging sensitive prompts or personal data.
- Centralize logging in "lib/logger.ts".
- Never send secrets, credentials, or private customer information to an AI provider unless the approved data-handling policy explicitly permits it.

7. Configuration and Environment Variables

- Declare required environment variables in ".env.example" with placeholder values and descriptions.
- Never commit real ".env" files or secrets.
- Prefix browser-exposed variables with "NEXT_PUBLIC_" only when public exposure is intentional.
- Read configuration through "lib/config.ts", not directly throughout components.
- Validate required environment variables at application startup or the appropriate server boundary.
- Do not use non-null assertions as a substitute for runtime validation.
- Never store secrets in "next.config.js" or "next.config.ts" public configuration.

8. Code Quality

- Do not leave commented-out code in pull requests.
- Use "// TODO(name): reason" only for actionable, justified deferred work.
- Never use "console.log" in production code; use the central logger.
- Prefer pure functions and isolate side effects.
- Name booleans with "is", "has", "can", or "should".
- Await asynchronous operations or explicitly handle intentionally detached promises.
- Use human-readable error messages without exposing raw internal exceptions.
- Avoid "eval()", unsanitized "dangerouslySetInnerHTML", and dynamic "require()".

9. Testing

- Use Vitest, not Jest.
- Run tests through "npm test".
- Place tests near the source when consistent with repository conventions.
- Add tests for exported utility functions and important behavioral changes.
- Mock Supabase, Groq, and external service calls in unit tests.
- Never call real paid AI APIs from ordinary unit tests.
- Cover error paths, invalid input, authorization boundaries, and retry behavior.
- Do not modify tests merely to conceal a genuine regression.

10. CI/CD Standards

The required pull-request validation order is:

1. Lint.
2. Type-check.
3. Unit and integration tests.
4. Build.

- Store workflows under ".github/workflows/".
- Use "package-lock.json" as the dependency lockfile.
- Cache npm downloads using the lockfile hash. Prefer "actions/setup-node" with npm caching when appropriate.
- Pin third-party actions to reviewed full commit SHAs for security-sensitive workflows.
- Set minimum required "GITHUB_TOKEN" permissions.
- Reference secrets through GitHub's secrets mechanism; never hardcode credentials.
- Notify Slack through "SLACK_WEBHOOK_URL" only when configured.
- Do not bypass required checks to force a green pipeline.
- Treat production deployment as a separately authorized operation.

11. Debugging Failed Jobs

Always follow this sequence:

Inspect → Classify → Diagnose → Repair → Rerun → Verify → Record

11.1 Inspect

Collect relevant evidence:

- Repository and workflow name.
- Workflow run ID and attempt number.
- Branch and commit SHA.
- Failed job and step.
- Sanitized error messages and annotations.
- Relevant dependency, runner, environment, and permission information.

Read only the logs necessary to diagnose the problem. Never publish secrets or sensitive log contents.

11.2 Classify

Use one of these categories:

- "code-defect"
- "lint"
- "type-check"
- "test-failure"
- "build-failure"
- "dependency"
- "cache"
- "network-transient"
- "runner-infrastructure"
- "permission"
- "missing-secret"
- "configuration"
- "timeout"
- "deployment"

Distinguish confirmed root causes from hypotheses.

11.3 Choose the Recovery Action

Failure| Recovery
Transient network failure| Retry only when safe and bounded
Runner interruption| Inspect state, then retry the affected job
Cache failure| Verify the cache key and dependencies
Lint or type-check error| Fix source or configuration
Test failure| Reproduce and fix the underlying defect
Build failure| Inspect compiler output and dependency versions
Permission or secret failure| Correct configuration through an authorized process
Production deployment failure| Stop, inspect deployment state, and require appropriate authorization

11.4 Safe Rerun Rules

- Prefer rerunning only failed jobs when successful jobs and their artifacts remain valid.
- Use a full workflow rerun only when dependencies, artifacts, or workflow semantics require it.
- Limit automatic retries to two attempts after the initial attempt unless an approved repository policy says otherwise.
- Use exponential backoff for suitable transient failures.
- Never automatically rerun deterministic code failures.
- Never automatically retry database migrations, destructive operations, or production deployments without an explicit safety mechanism and authorization.
- Verify repository, workflow, branch, commit, and run ID before requesting a rerun.
- Use the least-privileged credential available.
- Require GitHub Actions write permission for API-based reruns.
- Do not modify branch protection, disable security checks, or change permissions to make a rerun pass.

A successful rerun does not prove that an intermittent defect has been permanently fixed.

12. Recovery Observability

- Publish a concise GitHub Actions job summary.
- Record the run ID, attempt, failed job, failure category, remediation, and final outcome.
- Upload sanitized diagnostics only when useful.
- Preserve test reports and build evidence where appropriate.
- Avoid duplicate Slack notifications.
- Never print webhook URLs, tokens, credentials, or raw environment dumps.
- Do not convert failed steps into successful results without an explicit, justified policy.

13. Post-Rerun Verification

After recovery:

1. Confirm that GitHub accepted the rerun request.
2. Inspect the resulting workflow attempt and job conclusions.
3. Confirm that the successful result corresponds to the intended commit SHA.
4. Run the complete required validation sequence: lint → type-check → test → build.
5. Create an issue for recurring failures that require a durable fix.
6. Report any remaining uncertainty or risk.

Never claim that a rerun, test, or deployment succeeded without checking its actual result.

14. Git and Pull Requests

- Branch prefixes: "feat/", "fix/", "chore/", and "docs/".
- Use Conventional Commits, such as "feat(ai): add model routing".
- Reference the associated issue using "Closes #123" when appropriate.
- Keep pull requests focused on one logical change.
- Use Semantic Release for versioning; do not manually bump "package.json" versions.
- Do not push, merge, approve, release, or deploy without the required authorization.

15. Prohibited Patterns

- Do not suggest the legacy Next.js "pages/" router.
- Do not use "getServerSideProps" or "getStaticProps".
- Do not recommend Axios when native "fetch" or the approved SDK is sufficient.
- Do not manually generate Supabase migration files when the established workflow requires "supabase db diff".
- Do not add unexplained ESLint suppressions.
- Do not weaken RLS, authentication, branch protection, or required checks.
- Do not fabricate logs, test results, API responses, or deployment outcomes.

16. Required Reporting Format

For implementation work, report:

1. Summary of changes.
2. Files modified or added.
3. Design decisions and security considerations.
4. Tests and commands executed.
5. Actual test and validation results.
6. Rerun details, if applicable.
7. Outstanding issues and next steps.

For CI failures, additionally report the run ID, failed job and step, failure category, supporting evidence, proposed fix, rerun scope, and verified final outcome.

17. Final Rule

Inspect the existing repository before applying these conventions. Preserve working behavior, minimize changes, validate every important modification, and require explicit authorization for security-sensitive or production-impacting actions.