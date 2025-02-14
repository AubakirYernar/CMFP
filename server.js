const express = require('express');
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

const app = express();
const port = 3000;

// Middleware
app.use(express.static('public'));
app.use(express.json());

// Cleanup old plot images
setInterval(() => {
    const directory = 'public/images';
    fs.readdir(directory, (err, files) => {
        if (err) throw err;
        files.forEach(file => {
            if (file.endsWith('.png') && file.startsWith('task1_')) {
                const filePath = path.join(directory, file);
                const fileAge = (Date.now() - fs.statSync(filePath).mtimeMs) / 1000;
                if (fileAge > 300) { // Delete files older than 5 minutes
                    fs.unlinkSync(filePath);
                }
            }
        });
    });
}, 60000); // Run every minute

// Task 1 endpoint
app.post('/task1', (req, res) => {
    const python = spawn('python', ['python-scripts/cmf_1.py']);
    let output = '';
    
    python.stdin.write(JSON.stringify(req.body));
    python.stdin.end();
    
    python.stdout.on('data', (data) => output += data.toString());
    python.stderr.on('data', (data) => console.error(`Error: ${data}`));
    
    python.on('close', (code) => {
        if (code !== 0) {
            return res.status(500).json({ error: "Python script failed" });
        }
        try {
            res.json(JSON.parse(output));
        } catch (e) {
            res.status(500).json({ error: "Invalid JSON response" });
        }
    });
});


app.post('/task2', (req, res) => {
    const python = spawn('python', ['python-scripts/cmf_2.py']);
    let output = '';
    
    python.stdin.write(JSON.stringify(req.body));
    python.stdin.end();
    
    python.stdout.on('data', (data) => output += data.toString());
    python.stderr.on('data', (data) => console.error(`Error: ${data}`));
    
    python.on('close', (code) => {
        try {
            res.json(JSON.parse(output));
        } catch (e) {
            res.status(500).json({ error: "Calculation failed" });
        }
    });
});


app.post('/task3', (req, res) => {
    const python = spawn('python', ['python-scripts/cmf_3.py']);
    let output = '';
    
    python.stdin.write(JSON.stringify(req.body));
    python.stdin.end();
    
    python.stdout.on('data', (data) => output += data.toString());
    python.stderr.on('data', (data) => console.error(`Task3 error: ${data}`));
    
    python.on('close', (code) => {
        try {
            res.json(JSON.parse(output));
        } catch(e) {
            res.status(500).json({ 
                error: "Ошибка выполнения расчета",
                solution: null,
                iterations: 0
            });
        }
    });
});

app.post('/task4', (req, res) => {
    const python = spawn('python', ['python-scripts/cmf_4.py']);
    let output = '';
    
    python.stdin.write(JSON.stringify(req.body));
    python.stdin.end();
    
    python.stdout.on('data', (data) => output += data.toString());
    python.stderr.on('data', (data) => console.error(`Task4 error: ${data}`));
    
    python.on('close', (code) => {
        try {
            res.json(JSON.parse(output));
        } catch(e) {
            res.status(500).json({ error: "Matrix inversion failed" });
        }
    });
});

app.post('/task5', (req, res) => {
    const python = spawn('python', ['python-scripts/cmf_5.py']);
    let output = '';
    
    python.stdin.write(JSON.stringify(req.body));
    python.stdin.end();
    
    python.stdout.on('data', (data) => output += data.toString());
    python.stderr.on('data', (data) => console.error(`Task5 error: ${data}`));
    
    python.on('close', (code) => {
        try {
            res.json(JSON.parse(output));
        } catch(e) {
            res.status(500).json({ error: "Regression calculation failed" });
        }
    });
});

app.post('/task6', (req, res) => {
    const python = spawn('python', ['python-scripts/cmf_6.py']);
    let output = '';
    
    python.stdin.write(JSON.stringify(req.body));
    python.stdin.end();
    
    python.stdout.on('data', (data) => output += data.toString());
    python.stderr.on('data', (data) => console.error(`Task6 error: ${data}`));
    
    python.on('close', (code) => {
        try {
            res.json(JSON.parse(output));
        } catch(e) {
            res.status(500).json({ error: "Interpolation failed" });
        }
    });
});


app.post('/task7', (req, res) => {
    const python = spawn('python', ['python-scripts/cmf_7.py']);
    let output = '';
    
    python.stdin.write(JSON.stringify(req.body));
    python.stdin.end();
    
    python.stdout.on('data', (data) => output += data.toString());
    python.stderr.on('data', (data) => console.error(`Task7 error: ${data}`));
    
    python.on('close', (code) => {
        try {
            res.json(JSON.parse(output));
        } catch(e) {
            res.status(500).json({ error: "Calculation failed" });
        }
    });
});

app.post('/task8', (req, res) => {
    const python = spawn('python', ['python-scripts/cmf_8.py']);
    let output = '';
    
    python.stdin.write(JSON.stringify(req.body));
    python.stdin.end();
    
    python.stdout.on('data', (data) => output += data.toString());
    python.stderr.on('data', (data) => console.error(`Task8 error: ${data}`));
    
    python.on('close', (code) => {
        try {
            res.json(JSON.parse(output));
        } catch(e) {
            res.status(500).json({ error: "Integration failed" });
        }
    });
});


app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
    if (!fs.existsSync('public/images')) {
        fs.mkdirSync('public/images', { recursive: true });
    }
});