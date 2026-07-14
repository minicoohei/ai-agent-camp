---
nonInteractiveMode: incompatible
---

# Setup Google API for MCP - Google API Setup Guide

This command uses Cursor Browser to provide a step-by-step guide for Google API setup and OAuth 2.0 authentication for MCP (Model Context Protocol).

## Target APIs

- Gmail API
- Google Calendar API
- Google Drive API
- Google Sheets API

## Features

- **Cursor Browser utilization**: Semi-automate setup through browser operations
- **Step-by-step guide**: Proceed while checking status at each step
- **Clear user actions**: Explicitly indicate manual operations required for security
- **OAuth authentication flow**: From credential acquisition to authentication completion

## Execution Steps

### Phase 1: Confirm Parameters

Confirm the following information from the user's input:

1. **Target APIs** (multiple selection allowed):
   - `gmail` - Gmail API
   - `calendar` - Google Calendar API
   - `drive` - Google Drive API
   - `sheets` - Google Sheets API

2. **Project name** (optional, default: `mcp-google-api`)

3. **Output directory** (optional, default: project root)

### Phase 2: Google Cloud Console Setup (Cursor Browser)

Execute the following steps using Cursor Browser.

#### Step 1: Access Google Cloud Console

```
browser_navigate: https://console.cloud.google.com/
```

After execution, check the page state with `browser_snapshot` and verify login status.

**Guide the user:**
- If not logged in: "Please log in to your Google account"
- If already logged in: Proceed to the next step

#### Step 2: Create Project (if needed)

Can be skipped if using an existing project.

```
browser_navigate: https://console.cloud.google.com/projectcreate
```

**Guide the user:**
```
[Project Creation]
1. Enter a project name (recommended: mcp-google-api)
2. Select your organization (select "No organization" for personal accounts)
3. Click "Create"

Type "done" when ready.
```

#### Step 3: Enable APIs

Enable the selected APIs in order. URL pattern:

```
Gmail API:     https://console.cloud.google.com/apis/library/gmail.googleapis.com?project={PROJECT_ID}
Calendar API:  https://console.cloud.google.com/apis/library/calendar-json.googleapis.com?project={PROJECT_ID}
Drive API:     https://console.cloud.google.com/apis/library/drive.googleapis.com?project={PROJECT_ID}
Sheets API:    https://console.cloud.google.com/apis/library/sheets.googleapis.com?project={PROJECT_ID}
```

For each API page:
1. Navigate to the API page with `browser_navigate`
2. Check the page state with `browser_snapshot`
3. If the "Enable" button is found, guide the user to click it

**Guide the user:**
```
[API Enablement: {API name}]
Click the blue "Enable" button.
Type "done" when enablement is complete.
```

#### Step 4: OAuth Consent Screen Setup

```
browser_navigate: https://console.cloud.google.com/auth/overview?project={PROJECT_ID}
```

**Guide the user:**
```
[OAuth Consent Screen Setup]
1. Select "External" for user type and click "Create"
2. Enter the following information:
   - App name: Any name (e.g., MCP Google API)
   - User support email: Your email address
   - Developer contact information: Your email address
3. Click "Save and Continue"
4. On the Scopes screen, click "Save and Continue" as-is
5. On the Test Users screen, add your email address
6. Click "Save and Continue" -> "Back to Dashboard"

Type "done" when complete.
```

#### Step 5: Create OAuth Client ID

```
browser_navigate: https://console.cloud.google.com/auth/clients?project={PROJECT_ID}
```

**Guide the user:**
```
[OAuth Client ID Creation]
1. Click "+ Create Client" or "Create Credentials"
2. Application type: Select "Desktop app"
3. Name: Any name (e.g., MCP Desktop Client)
4. Click "Create"
5. In the dialog that appears, click "Download JSON"
6. Save the downloaded file to a safe location

Please provide the path to the JSON file
(macOS example: ~/Downloads/client_secret_xxx.json)
(Windows WSL2 example: /mnt/c/Users/<WindowsUserName>/Downloads/client_secret_xxx.json)
```

### Phase 3: Execute OAuth Authentication Flow

Use the downloaded credential JSON to execute the authentication flow.

```bash
uv run python tools/google_api_setup.py auth \
  --credentials "{credential_json_path}" \
  --scopes "{selected_scopes}" \
  --output "{output_directory}"
```

**Scope mapping:**
- gmail: `https://www.googleapis.com/auth/gmail.readonly,https://www.googleapis.com/auth/gmail.modify`
- calendar: `https://www.googleapis.com/auth/calendar,https://www.googleapis.com/auth/calendar.events`
- drive: `https://www.googleapis.com/auth/drive`
- sheets: `https://www.googleapis.com/auth/spreadsheets`

### Phase 4: Completion Confirmation

Upon successful authentication, the following files are generated:
- `token.json` - Authentication token
- `mcp_config.json` - MCP configuration file (reference)

**Report to the user:**
```
[Setup Complete]
Google API setup is complete!

Generated files:
- token.json: Authentication token (important: keep this secure)
- mcp_config.json: MCP configuration example

Next steps:
1. Edit the MCP server configuration file
2. Set the path of the generated token in the configuration
3. Start the MCP server and test

Refer to each MCP server's documentation for detailed MCP configuration instructions.
```

## Usage Examples

### Basic usage (all APIs)
```
/setup-google-api gmail calendar drive sheets
```

### Specific APIs only
```
/setup-google-api gmail sheets
```

### Specify project name
```
/setup-google-api gmail --project my-mcp-project
```

## Notes

### Security Precautions
- **Never expose the credential JSON or token.json**
- With these files, anyone can access your Google account
- Add them to `.gitignore` to prevent committing to the repository

### Actions Requiring User Intervention
The following actions must be performed by the user for security reasons:
1. Logging in to a Google account
2. Granting permissions on the OAuth consent screen
3. Downloading the credential JSON
4. Approving in the browser during the authentication flow

### Troubleshooting

#### Error: "Access blocked: This app's request is invalid"
- The OAuth consent screen setup may not be complete
- Verify that your email address has been added as a test user

#### Error: "invalid_grant"
- The token.json may have become invalid
- Delete token.json and run the authentication flow again

#### Error: "API not enabled"
- The required API may not be enabled
- Verify that the API is enabled in Google Cloud Console
