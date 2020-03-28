const WIDTH = 500;
const HEIGHT = 500;
let BOX_SIZE = 100;
const MIN_SPACING = 25;
let POP_NUM = 5;
let DAYS_CURE = 700;
let INFECTION_RADIUS = 50;
let INFECTION_PROB = 100; // 100 in 1000 or 10 %

let box_list = [];
// an array to add multiple particles
let particles = [];
let input, button;

function calc_boxes() {
    let positions = [];
    console.log('INSIDE CALC', BOX_SIZE);
    let max_per_row = floor(WIDTH / (BOX_SIZE + MIN_SPACING));
    let max_per_col = floor(HEIGHT / (BOX_SIZE + MIN_SPACING));
    let ext_spc_row = (WIDTH - max_per_row * BOX_SIZE) / (max_per_row + 1);
    let ext_spc_col = (HEIGHT - max_per_row * BOX_SIZE) / (max_per_row + 1);

    let box_spc_row = ext_spc_row;
    let box_spc_col = ext_spc_col;

    for (let i = 1; i <= max_per_col; i++) {
        for (let j = 1; j <= max_per_row; j++) {
            let x = i * (box_spc_col) + (i - 1) * (BOX_SIZE);
            let y = j * (box_spc_row) + (j - 1) * (BOX_SIZE);
            positions.push([x, y]);
        }
    }
    console.log(positions);
    return positions
}

function mybox(x, y) {
    // console.log('box called');
    stroke(255, 255, 255);
    fill(100, 100, 100, 0);
    square(x, y, BOX_SIZE);
}

function populate_boxes(box_l) {
    particles.push(new Particle(box_list[0][0], box_list[0][1], BOX_SIZE, true));

    for (let b = 0; b < box_list.length; b++) {
        for (let i = 0; i < POP_NUM; i++) {
            particles.push(new Particle(box_list[b][0], box_list[b][1], BOX_SIZE, false));
        }
    }
}

function setup() {
    createCanvas(WIDTH, HEIGHT);

    input = createInput(BOX_SIZE);
    input.position(WIDTH+50, 30);
    let boxlabel = createElement('h2', 'Tamanho das caixas');
    boxlabel.position(input.x, input.y - 45);

    label_slider_inf_prob = createElement('p');
    label_slider_inf_prob.position(input.x, input.y + 30);
    slider_inf_prob = createSlider(0, 100, INFECTION_PROB / 10, 5);
    slider_inf_prob.position(input.x, label_slider_inf_prob.y + 45);

    label_slider_inf_radius = createElement('p');
    label_slider_inf_radius.position(input.x, slider_inf_prob.y + 30);
    slider_inf_radius = createSlider(0, 100, INFECTION_RADIUS, 5);
    slider_inf_radius.position(input.x, label_slider_inf_radius.y + 45);

    label_slider_days_cure = createElement('p');
    label_slider_days_cure.position(input.x, slider_inf_radius.y + 30);
    slider_inf_days_cure = createSlider(0, 1000, DAYS_CURE, 50);
    slider_inf_days_cure.position(input.x, label_slider_days_cure.y + 45);

    label_slider_population = createElement('p');
    label_slider_population.position(input.x, slider_inf_days_cure.y + 30);
    slider_inf_population = createSlider(0, 50, POP_NUM, 1);
    slider_inf_population.position(input.x, label_slider_population.y + 45);


    normallabel = createElement('h2', 'Normal: ' + particles.length);
    normallabel.position(input.x, slider_inf_population.y + 50);
    infectedlabel = createElement('h2', 'Infectados: ' + particles.length);
    infectedlabel.position(input.x, normallabel.y + 50);
    recoveredlabel = createElement('h2', 'Recuperados: ' + particles.length);
    recoveredlabel.position(input.x, infectedlabel.y + 50);

    button = createButton('Restart');
    button.position(input.x + input.width + 5, input.y);
    button.mousePressed(update_sim);

    box_list = calc_boxes();

    populate_boxes(box_list);

    textAlign(CENTER);
    textSize(50);
}

function draw() {
    background('#2a2a2a');
    for (let i = 0; i < box_list.length; i++) {
        mybox(box_list[i][0], box_list[i][1]);
    }
    for (let i = 0; i < particles.length; i++) {
        particles[i].colorParticle();
        particles[i].updateParticle();
        // particles[i].joinParticles(particles.slice(i));
        particles[i].infectParticles(particles);
    }
    update_labels();
}

function update_sim() {
    const number = input.value();
    BOX_SIZE = parseInt(number);
    INFECTION_PROB = parseInt(slider_inf_prob.value()) * 10;
    INFECTION_RADIUS = parseInt(slider_inf_radius.value());
    DAYS_CURE = parseInt(slider_inf_days_cure.value());
    POP_NUM = parseInt(slider_inf_population.value());

    console.log('infeciton', INFECTION_PROB);
    console.log(BOX_SIZE, number);

    box_list = calc_boxes();
    console.log('new_box', box_list);
    particles = [];
    populate_boxes(box_list);

}

function update_labels() {
    let normal = 0;
    let infected = 0;
    let recovered = 0;

    for (let p = 0; p < particles.length; p++) {
        switch (particles[p].health) {
            case 0:
                normal++;
                break;
            case 1:
                infected++;
                break;
            case 2:
                recovered++;
                break;
        }
    }
    label_slider_inf_prob.html('Probabilidade de contaminação: ' + slider_inf_prob.value());
    label_slider_inf_radius.html('Raio de contaminação: ' + slider_inf_radius.value());
    label_slider_days_cure.html('Dias para cura: ' + slider_inf_days_cure.value());
    label_slider_population.html('População por caixa: ' + slider_inf_population.value());

    normallabel.html('Normal: ' + normal);
    infectedlabel.html('Infectados: ' + infected);
    recoveredlabel.html('Recuperados: ' + recovered);
}