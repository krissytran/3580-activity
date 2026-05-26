# Intentionally Insecure Minesweeper App
## Educational Example of Security Vulnerabilities

⚠️ **WARNING**: This application is intentionally built with security vulnerabilities for educational purposes. These are **examples of what NOT to do**. DO NOT use these patterns in production code.

## Overview

This is a full-stack Minesweeper application that demonstrates:
- **44+ security vulnerabilities** across frontend and backend
- **Common attack patterns** including SQL injection, XSS, and more
- **Bad practices** to learn what to avoid

## Quick Start

```bash
# Install dependencies
npm install

# Run the server
npm start

# Open browser to http://localhost:3000
```

## Features (All Intentionally Insecure)

✗ SQL Injection vulnerable authentication
✗ Plain text password storage
✗ Credentials in source code
✗ Client-side game logic
✗ Credentials in localStorage
✗ No CSRF protection
✗ No rate limiting
✗ Excessive CORS permissions
✗ File upload path traversal
✗ Weak admin panel
... and 34 more vulnerabilities!

## Structure

```
.
├── server.js           # Node/Express backend with vulnerabilities
├── public/
│   └── index.html      # Frontend with vulnerabilities
├── game.db             # SQLite database (NOT in real .gitignore for demo)
├── package.json        # Dependencies
└── VULNERABILITIES.md  # Detailed list of all issues
```

## Learning Objectives

This application teaches you:

1. **SQL Injection**: See how direct string concatenation in queries is exploited
2. **Authentication**: Understand why passwords must be hashed
3. **Client-Side Security**: Learn what should NEVER be computed on the client
4. **Data Exposure**: Recognize when sensitive information is exposed
5. **Input Validation**: Understand why validation must happen server-side
6. **CSRF Protection**: See why state-changing requests need tokens
7. **Error Handling**: Learn why detailed errors aid attackers
8. **Secrets Management**: Understand why credentials need to be in environment variables
9. **Session Management**: Learn about secure cookie and token handling
10. **Authorization**: Understand access control and resource ownership

## How to Exploit This App

### SQL Injection
```
Username: admin' OR '1'='1
Password: anything
```
Result: Logs in without correct password!

### View All Passwords
1. Open browser DevTools
2. Go to Application tab
3. Check localStorage - passwords are there!

### See Mine Locations
1. Open DevTools
2. Start a game
3. Check the Network tab - entire board sent in response
4. Check the data attributes on cells - mines are visible!

### Bypass Admin Panel
1. Try common passwords for admin endpoint
2. No rate limiting = easy brute force

## Try These Experiments

### Experiment 1: SQL Injection
- Try `admin' --` as username
- Try `admin' UNION SELECT * FROM users --`

### Experiment 2: Client-Side Manipulation
- Open DevTools Console
- Type: `localStorage.getItem('password')`
- See the password in plain text!

### Experiment 3: Game Logic Bypass
- Start a game
- Open DevTools
- Type: `currentBoard` to see all mine locations
- Click cells knowing where the mines are

### Experiment 4: Path Traversal
- Request: `GET /api/files/../../../../etc/passwd`
- Potentially access files outside intended directory

## Remediation Examples

See `VULNERABILITIES.md` for detailed fixes for each issue.

## Security Best Practices (Do's)

✅ Use parameterized queries (prepared statements)
✅ Hash passwords with bcrypt or Argon2
✅ Store secrets in environment variables
✅ Use cryptographically secure random generation
✅ Validate and sanitize ALL user input
✅ Implement CSRF token protection
✅ Use HTTPOnly, Secure, SameSite cookies
✅ Implement rate limiting
✅ Restrict CORS appropriately
✅ Return generic error messages
✅ Enforce HTTPS
✅ Keep dependencies updated
✅ Log securely (never log secrets)
✅ Implement proper authentication/authorization
✅ Use security headers
✅ Implement Content Security Policy
✅ Server-side validation ALWAYS
✅ Principle of least privilege
✅ Regular security audits
✅ Encrypt sensitive data

## Disclaimer

This application is for **educational purposes only**. It demonstrates vulnerabilities that should be fixed before ANY application goes to production. Never use these patterns in real applications!

## Further Reading

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE - Common Weakness Enumeration](https://cwe.mitre.org/)
- [PortSwigger Web Security Academy](https://portswigger.net/web-security)
- [SANS Top 25](https://www.sans.org/top25-software-errors/)

## Author

This intentionally vulnerable application was created as an educational tool to teach security concepts.
