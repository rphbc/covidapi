// this class describes the properties of a single particle.
class Particle {
// setting the co-ordinates, radius and the
// speed of a particle in both the co-ordinates axes.
    constructor(limit_x, limit_y, size, infected) {
        this.limit_x = limit_x;
        this.limit_y = limit_y;
        this.size = size;
        this.x = random(this.limit_x, this.limit_x + this.size);
        this.y = random(this.limit_y, this.limit_y + this.size);
        this.r = 8;
        this.xSpeed = random(-2, 2);
        this.ySpeed = random(-2, 2);

        // 0 for normal, 1 for infected, 2 for recovered, 3 for dead
        if (infected) {
            this.health = 1;
        }
        else {
            this.health = 0;
        }

        this.infected_age = 0;
    }

// creation of a particle.
    colorParticle() {
        switch (this.health){
            case 0:
                noStroke();
                fill('rgba(12,50,196,0.5)');
                circle(this.x, this.y, this.r);
                break;
            case 1:
                noStroke();
                fill('rgba(174,0,0,0.5)');
                circle(this.x, this.y, this.r);
                break;
            case 2:
                noStroke();
                fill('rgba(56,200,52,0.5)');
                circle(this.x, this.y, this.r);
                break;
            case 3:
                noStroke();
                fill('rgba(42,42,42,0.5)');
                circle(this.x, this.y, this.r);
                break;
        }
    }

// setting the particle in motion.
    updateParticle() {
        if (this.x < this.limit_x || this.x > (this.limit_x + this.size))
            this.xSpeed *= -1;
        if (this.y < this.limit_y || this.y > (this.limit_y + this.size))
            this.ySpeed *= -1;
        this.x += this.xSpeed;
        this.y += this.ySpeed;

        if (this.infected_age > DAYS_CURE){
            this.health = 2;
        }

        if (this.health === 1){
            this.infected_age++;
        }
    }

// this function creates the connections(lines)
// between particles which are less than a certain distance apart
    joinParticles(particles) {
        particles.forEach(element => {
            let dis = dist(this.x, this.y, element.x, element.y);
            if (dis < 85) {
                stroke('rgba(255,255,255,0.04)');
                line(this.x, this.y, element.x, element.y);
            }
        });
    }

    infectParticles(particles){
        particles.forEach(element => {
            let dis = dist(this.x, this.y, element.x, element.y);
            if (dis < INFECTION_RADIUS) {
                stroke('rgba(255,255,255,0.4)');
                line(this.x, this.y, element.x, element.y);
                if (this.health === 1 && random(0,1000) <= INFECTION_PROB
                    && element.health === 0){
                    // console.log('spread infection');
                    element.health = 1;
                }
            }
        });
    }
}
