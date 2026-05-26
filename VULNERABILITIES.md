# Security Vulnerabilities in This Application

**WARNING**: This application is intentionally built with security flaws for educational purposes. These are examples of **WHAT NOT TO DO**.

## Server-Side Vulnerabilities

### 1. **SQL Injection (CRITICAL)**
- **Lines**: server.js lines 68-70, 95-97, 130-132
- **Issue**: Direct string concatenation in SQL queries
- **Attack**: `' OR '1'='1`
- **Fix**: Use prepared statements/parameterized queries

### 2. **Plain Text Password Storage (CRITICAL)**
- **Lines**: server.js lines 92-96
- **Issue**: Passwords stored unencrypted in database
- **Attack**: Database breach exposes all user credentials
- **Fix**: Hash passwords with bcrypt, Argon2, or similar

### 3. **Credentials in Source Code (CRITICAL)**
- **Lines**: server.js lines 50-51
- **Issue**: Hardcoded admin password and secret key
- **Attack**: Exposed in version control
- **Fix**: Use environment variables

### 4. **Weak Random Number Generation (HIGH)**
- **Lines**: server.js line 155
- **Issue**: Using Math.random() for security-sensitive operations
- **Fix**: Use crypto.getRandomValues() or crypto.randomBytes()

### 5. **Missing Input Validation (HIGH)**
- **Lines**: server.js lines 62-64, 87-88
- **Issue**: No validation of game dimensions or parameters
- **Attack**: Negative values, extremely large values causing DoS
- **Fix**: Validate all user inputs on server side

### 6. **No CSRF Protection (MEDIUM)**
- **Lines**: server.js line 103
- **Issue**: No CSRF tokens on state-changing requests
- **Fix**: Implement CSRF token validation

### 7. **Missing Authentication (MEDIUM)**
- **Lines**: server.js lines 114-127
- **Issue**: No authentication required for game endpoints
- **Fix**: Verify user identity before processing requests

### 8. **No Authorization Checks (MEDIUM)**
- **Lines**: server.js lines 114-127, 137-148
- **Issue**: Users can access other players' games
- **Fix**: Verify user owns the resource they're accessing

### 9. **No Rate Limiting (MEDIUM)**
- **Lines**: server.js line 105
- **Issue**: Unlimited requests to endpoints
- **Attack**: Brute force, DoS attacks
- **Fix**: Implement rate limiting middleware

### 10. **Excessive CORS Permissions (MEDIUM)**
- **Lines**: server.js line 15
- **Issue**: `cors()` allows ANY origin to access the API
- **Fix**: Specify allowed origins explicitly

### 11. **Exposing Error Details (MEDIUM)**
- **Lines**: server.js lines 71, 98, 125, 142
- **Issue**: Returning raw database error messages to clients
- **Attack**: Information disclosure about database structure
- **Fix**: Log errors server-side, return generic error messages to client

### 12. **No Sensitive Data Encryption (MEDIUM)**
- **Lines**: server.js lines 26-31, 62-72
- **Issue**: Game board (including mine locations) sent to client
- **Attack**: Client can view all mine locations before clicking
- **Fix**: Calculate logic server-side, only send revealed cells

### 13. **Outdated Dependencies (MEDIUM)**
- **Lines**: package.json
- **Issue**: Using very old versions of express, body-parser
- **Fix**: Keep dependencies up to date

### 14. **Insufficient Logging (LOW)**
- **Lines**: server.js line 165
- **Issue**: Logging credentials to console
- **Fix**: Never log sensitive information

### 15. **No HTTPS Enforcement (MEDIUM)**
- **Lines**: server.js line 164
- **Issue**: Server runs on HTTP only
- **Fix**: Enforce HTTPS in production

### 16. **File Upload Vulnerability (HIGH)**
- **Lines**: server.js lines 133-137
- **Issue**: Path traversal possible via /api/files endpoint
- **Attack**: `../../../etc/passwd`
- **Fix**: Validate and sanitize file paths, use whitelist

### 17. **Weak Admin Authentication (MEDIUM)**
- **Lines**: server.js lines 139-145
- **Issue**: Simple string comparison for admin password
- **Fix**: Use proper authentication/authorization framework

### 18. **Dangerous Admin Endpoints (HIGH)**
- **Lines**: server.js lines 151-158
- **Issue**: Delete all games with minimal protection
- **Fix**: Require confirmation, audit logging, role-based access

## Client-Side Vulnerabilities

### 19. **XSS Vulnerability (MEDIUM)**
- **Lines**: index.html lines 181, 200
- **Issue**: Unsanitized user input displayed in alerts
- **Attack**: `' + alert('xss') + '`
- **Fix**: Use textContent instead of innerHTML, sanitize output

### 20. **Credentials in localStorage (CRITICAL)**
- **Lines**: index.html lines 161-167
- **Issue**: Storing sensitive data in localStorage
- **Attack**: XSS attacks can steal all credentials
- **Fix**: Use httpOnly cookies for session management

### 21. **No Session Timeout (MEDIUM)**
- **Lines**: index.html line 267
- **Issue**: Session persists indefinitely in localStorage
- **Fix**: Implement session expiration

### 22. **Storing Passwords in Memory (MEDIUM)**
- **Lines**: index.html lines 161-167
- **Issue**: Password stored in localStorage
- **Fix**: Never store passwords client-side

### 23. **Game Logic on Client (HIGH)**
- **Lines**: index.html lines 234-248
- **Issue**: Entire game board state stored in client
- **Attack**: Inspect with DevTools, modify board state
- **Fix**: Keep game logic server-side

### 24. **Data Attributes Exposure (LOW)**
- **Lines**: index.html line 230
- **Issue**: Mine locations in data attributes
- **Attack**: Inspect element reveals all mines
- **Fix**: Compute on server, don't store on client

### 25. **No Input Validation (MEDIUM)**
- **Lines**: index.html lines 76-79, 191-194
- **Issue**: No client-side validation of dimensions
- **Fix**: Add validation before sending to server

## Infrastructure Issues

### 26. **Database in Root Directory (LOW)**
- **Lines**: server.js line 54
- **Issue**: SQLite database tracked in version control
- **Fix**: Add to .gitignore, use proper database server

### 27. **No Environment Configuration (MEDIUM)**
- **Issue**: Port, database path hardcoded
- **Fix**: Use environment variables

### 28. **No Logging/Monitoring (MEDIUM)**
- **Issue**: No audit trail of user actions
- **Fix**: Implement comprehensive logging

## Recommended Fixes (Production Checklist)

- ✅ Use prepared statements for ALL database queries
- ✅ Hash passwords with bcrypt (cost factor 12+)
- ✅ Move secrets to environment variables
- ✅ Use crypto.getRandomValues() or crypto.randomBytes()
- ✅ Validate ALL user inputs server-side
- ✅ Implement CSRF token protection
- ✅ Use JWT or secure session cookies (httpOnly, Secure, SameSite)
- ✅ Implement rate limiting
- ✅ Restrict CORS to specific origins
- ✅ Return generic error messages
- ✅ Use HTTPS everywhere
- ✅ Keep dependencies up to date
- ✅ Implement proper logging (never log secrets)
- ✅ Use Web Application Firewall (WAF)
- ✅ Regular security audits and penetration testing
- ✅ Implement Content Security Policy (CSP)
- ✅ Use security headers (X-Frame-Options, X-Content-Type-Options, etc.)
- ✅ Implement proper authentication/authorization
- ✅ Use encrypted HTTPS connections
- ✅ Store sensitive files outside web root
