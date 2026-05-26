const express = require('express');
const bodyParser = require('body-parser');
const sqlite3 = require('sqlite3');
const cors = require('cors');
const path = require('path');

const app = express();

// VULNERABILITY 1: Using outdated middleware versions
// VULNERABILITY 2: Not setting proper CORS restrictions
app.use(cors()); // Allows requests from ANY origin

// VULNERABILITY 3: Not validating Content-Type
app.use(bodyParser.json({ limit: '50mb' })); // Huge payload limit
app.use(bodyParser.urlencoded({ limit: '50mb', extended: true }));

// Serve static files
app.use(express.static('public'));

// VULNERABILITY 4: Database stored in version control
const db = new sqlite3.Database('./game.db');

// VULNERABILITY 5: No error handling
db.run(`CREATE TABLE IF NOT EXISTS games (
  id TEXT PRIMARY KEY,
  board TEXT,
  revealed TEXT,
  gameStatus TEXT,
  userId TEXT,
  createdAt DATETIME
)`);

db.run(`CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY,
  username TEXT UNIQUE,
  password TEXT,
  score INTEGER
)`);

db.run(`CREATE TABLE IF NOT EXISTS scores (
  id INTEGER PRIMARY KEY,
  username TEXT,
  score INTEGER,
  timestamp DATETIME
)`);

// VULNERABILITY 6: Credentials hardcoded
const ADMIN_PASSWORD = 'admin123';
const SECRET_KEY = 'my-secret-key-12345';

// VULNERABILITY 7: No input validation on login
app.post('/api/login', (req, res) => {
  const { username, password } = req.body;
  
  // VULNERABILITY 8: SQL Injection - concatenating user input directly into query
  const query = `SELECT * FROM users WHERE username = '${username}' AND password = '${password}'`;
  
  db.get(query, (err, row) => {
    if (err) {
      res.status(500).json({ error: err.message });
      return;
    }
    
    if (row) {
      // VULNERABILITY 9: Storing password in response/session unencrypted
      res.json({ 
        success: true, 
        userId: row.id, 
        username: row.username,
        password: row.password // NEVER do this!
      });
    } else {
      res.status(401).json({ error: 'Invalid credentials' });
    }
  });
});

// VULNERABILITY 10: No authentication on endpoint
app.post('/api/register', (req, res) => {
  const { username, password } = req.body;
  
  // VULNERABILITY 11: Plain text password storage
  const insertQuery = `INSERT INTO users (username, password, score) VALUES ('${username}', '${password}', 0)`;
  
  db.run(insertQuery, (err) => {
    if (err) {
      // VULNERABILITY 12: Exposing sensitive error messages
      res.status(400).json({ error: err.message });
      return;
    }
    res.json({ success: true, message: 'User registered' });
  });
});

// VULNERABILITY 13: Random ID generation not cryptographically secure
function generateGameId() {
  return Math.random().toString(36).substring(2, 15);
}

// VULNERABILITY 14: No CSRF protection
app.post('/api/game/new', (req, res) => {
  const { width = 10, height = 10, mines = 10, userId } = req.body;
  
  // VULNERABILITY 15: No input sanitization
  const board = createBoard(width, height, mines);
  const gameId = generateGameId();
  
  const insertQuery = `INSERT INTO games (id, board, revealed, gameStatus, userId, createdAt) VALUES ('${gameId}', '${JSON.stringify(board)}', '${JSON.stringify(createEmptyBoard(width, height))}', 'playing', '${userId}', datetime('now'))`;
  
  db.run(insertQuery, (err) => {
    if (err) {
      res.status(500).json({ error: err.message });
      return;
    }
    // VULNERABILITY 16: Sending entire board (including mine locations) to client
    res.json({ gameId, board, width, height, mines });
  });
});

// VULNERABILITY 17: No rate limiting
app.post('/api/game/:gameId/click', (req, res) => {
  const { gameId } = req.params;
  const { x, y } = req.body;
  
  // VULNERABILITY 18: SQL Injection in SELECT
  const query = `SELECT * FROM games WHERE id = '${gameId}'`;
  
  db.get(query, (err, game) => {
    if (err || !game) {
      res.status(404).json({ error: 'Game not found' });
      return;
    }
    
    const board = JSON.parse(game.board);
    const revealed = JSON.parse(game.revealed);
    
    // VULNERABILITY 19: Revealing mine locations to client
    if (board[y][x] === 'M') {
      revealed[y][x] = 'M';
      // VULNERABILITY 20: Sending entire board on game over
      res.json({ gameOver: true, revealed: board });
      return;
    }
    
    const count = countAdjacentMines(board, x, y);
    revealed[y][x] = count;
    
    // VULNERABILITY 21: No validation before updating
    const updateQuery = `UPDATE games SET revealed = '${JSON.stringify(revealed)}' WHERE id = '${gameId}'`;
    
    db.run(updateQuery, (err) => {
      if (err) {
        res.status(500).json({ error: err.message });
        return;
      }
      res.json({ revealed, gameOver: false });
    });
  });
});

// VULNERABILITY 22: No authorization checks
app.get('/api/game/:gameId', (req, res) => {
  const { gameId } = req.params;
  const query = `SELECT * FROM games WHERE id = '${gameId}'`;
  
  db.get(query, (err, game) => {
    if (err || !game) {
      res.status(404).json({ error: 'Game not found' });
      return;
    }
    
    // VULNERABILITY 23: Returning board state including mines
    res.json(JSON.parse(game.board));
  });
});

// VULNERABILITY 24: Direct file access without validation
app.get('/api/files/:filename', (req, res) => {
  const filename = req.params.filename;
  res.sendFile(path.join(__dirname, 'uploads', filename));
});

// VULNERABILITY 25: Admin endpoint with weak password check
app.post('/api/admin/scores', (req, res) => {
  const { password } = req.body;
  
  if (password !== ADMIN_PASSWORD) {
    res.status(401).json({ error: 'Unauthorized' });
    return;
  }
  
  // VULNERABILITY 26: Full database dump endpoint
  db.all('SELECT * FROM scores', (err, rows) => {
    if (err) {
      res.status(500).json({ error: err.message });
      return;
    }
    res.json(rows);
  });
});

// VULNERABILITY 27: Clearing database without confirmation
app.post('/api/admin/reset', (req, res) => {
  db.run('DELETE FROM games', (err) => {
    if (err) {
      res.status(500).json({ error: err.message });
      return;
    }
    res.json({ success: true });
  });
});

// Helper functions
function createBoard(width, height, mines) {
  const board = Array(height).fill(null).map(() => Array(width).fill(0));
  let minesPlaced = 0;
  
  while (minesPlaced < mines) {
    // VULNERABILITY 28: Weak random number generation
    const x = Math.floor(Math.random() * width);
    const y = Math.floor(Math.random() * height);
    
    if (board[y][x] !== 'M') {
      board[y][x] = 'M';
      minesPlaced++;
    }
  }
  
  return board;
}

function createEmptyBoard(width, height) {
  return Array(height).fill(null).map(() => Array(width).fill('?'));
}

function countAdjacentMines(board, x, y) {
  let count = 0;
  for (let dy = -1; dy <= 1; dy++) {
    for (let dx = -1; dx <= 1; dx++) {
      const ny = y + dy;
      const nx = x + dx;
      if (ny >= 0 && ny < board.length && nx >= 0 && nx < board[0].length) {
        if (board[ny][nx] === 'M') count++;
      }
    }
  }
  return count;
}

// VULNERABILITY 29: No HTTPS enforcement
// VULNERABILITY 30: Logging sensitive information
app.listen(3000, () => {
  console.log('Server running on http://localhost:3000');
  console.log('Admin password:', ADMIN_PASSWORD);
  console.log('Secret key:', SECRET_KEY);
});
