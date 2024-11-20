const config = {
    type: Phaser.AUTO,
    width: 800,
    height: 600,
    backgroundColor: '#FFFFFF',
    parent: 'gameContainer',
    physics: {
        default: 'arcade',
        arcade: {
            gravity: { y: 0 },
            debug: false
        }
    },
    scene: {
        preload: preload,
        create: create,
        update: update
    }
};

const game = new Phaser.Game(config);

// Global game variables
let cube;
let gates;
let score = 0;
let scoreText;
let timeLeft = 15; // Countdown timer in seconds
let timerText;
let cursors;
let gameStarted = false;
let highScoresList = [
    { initials: "GJD", score: 23 },
    { initials: "ADC", score: 22 },
    { initials: "MLK", score: 20 },
    { initials: "JFK", score: 16 },
    { initials: "BUT", score: 12 }
];

// Load assets
function preload() {
    this.load.image('cube', 'Character.png'); // Replace with your character image path
}

// Create game objects
function create() {
    cursors = this.input.keyboard.createCursorKeys();

    // Set up cube
    cube = this.physics.add.sprite(400, 500, 'cube');
    cube.setCollideWorldBounds(true);

    // Set up gates group and add first gates
    gates = this.physics.add.group();
    createGate(this, 200, 'RED');
    createGate(this, 600, 'GREEN');

    // Display score and timer
    scoreText = this.add.text(16, 16, `Score: ${score}`, { fontSize: '32px', fill: '#000' });
    timerText = this.add.text(650, 16, `Time: ${timeLeft}`, { fontSize: '32px', fill: '#000' });

    // Set up timer for countdown
    this.time.addEvent({
        delay: 1000,
        callback: () => {
            if (gameStarted) {
                timeLeft -= 1;
                timerText.setText(`Time: ${timeLeft}`);
                if (timeLeft <= 0) {
                    endGame(this);
                }
            }
        },
        loop: true
    });

    // Collision detection between cube and gates
    this.physics.add.overlap(cube, gates, collectGate, null, this);
}

// Update game objects every frame
function update() {
    if (gameStarted) {
        // Cube movement
        if (cursors.left.isDown) {
            cube.setVelocityX(-200);
        } else if (cursors.right.isDown) {
            cube.setVelocityX(200);
        } else {
            cube.setVelocityX(0);
        }

        // Make gates fall and reset when they go out of bounds
        Phaser.Actions.Call(gates.getChildren(), (gate) => {
            gate.y += gate.speed;
            if (gate.y > 600) {
                resetGate(gate);
            }
        });
    }
}

// Helper function to create gates
function createGate(scene, x, color) {
    const gate = scene.add.rectangle(x, 0, 100, 40, color === 'RED' ? 0xff0000 : 0x00ff00);
    scene.physics.add.existing(gate);
    gate.body.setAllowGravity(false);
    gate.body.immovable = true;
    gate.speed = 2; // Speed of falling
    gate.answer = randomEquation();
    gates.add(gate);
}

// Helper function to reset gates
function resetGate(gate) {
    gate.y = 0;
    gate.x = Phaser.Math.Between(100, 700);
    gate.fillColor = Phaser.Math.Between(0, 1) ? 0xff0000 : 0x00ff00;
    gate.answer = gate.fillColor === 0xff0000 ? randomEquation() : randomEquation();
}

// Collision handler for collecting gates
function collectGate(cube, gate) {
    score += gate.answer;
    scoreText.setText(`Score: ${score}`);
    resetGate(gate);
}

// Function for ending the game and showing the high score screen
function endGame(scene) {
    gameStarted = false;
    scene.add.text(300, 250, "Game Over", { fontSize: '48px', fill: '#000' });
    scene.add.text(280, 320, `Final Score: ${score}`, { fontSize: '32px', fill: '#000' });

    // Check if score qualifies for high scores
    if (score > highScoresList[highScoresList.length - 1].score) {
        const initials = prompt("New High Score! Enter your initials:");
        highScoresList.push({ initials, score });
        highScoresList.sort((a, b) => b.score - a.score);
        highScoresList = highScoresList.slice(0, 5); // Keep only top 5 scores
    }

    displayHighScores(scene);
}

// Function to display high scores
function displayHighScores(scene) {
    scene.add.text(300, 50, "High Scores", { fontSize: '48px', fill: '#000' });
    highScoresList.forEach((entry, index) => {
        scene.add.text(300, 100 + index * 40, `${entry.initials}: ${entry.score}`, { fontSize: '32px', fill: '#000' });
    });
    scene.add.text(300, 400, "Press F5 to Restart", { fontSize: '24px', fill: '#000' });
}

// Randomly generates an equation answer for gates
function randomEquation() {
    const equations = [4, 6, 3, 9, -2, 8, 3, 9, -3, -5]; // Example answers
    return Phaser.Utils.Array.GetRandom(equations);
}

