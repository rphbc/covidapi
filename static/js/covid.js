const WIDTH = 500;
const HEIGHT = 500;
let BOX_SIZE = 60;
const MIN_SPACING = 20;
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
    let max_per_row = floor(WIDTH / (BOX_SIZE + MIN_SPACING)) -1 ;
    let max_per_col = floor(HEIGHT / (BOX_SIZE + MIN_SPACING)) - 1;
    let ext_spc_row = (WIDTH - (max_per_row)* BOX_SIZE) / (max_per_row+1);
    let ext_spc_col = (HEIGHT - (max_per_row)* BOX_SIZE) / (max_per_row+1);

    console.log(max_per_row, max_per_col, ext_spc_row, ext_spc_col);
    debugger

    let box_spc_row = ext_spc_row;
    let box_spc_col = ext_spc_col;

    for (let i = 1; i <= max_per_row; i++) {
        for (let j = 1; j <= max_per_col; j++) {
            let x = i * (box_spc_row) + (i - 1) * (BOX_SIZE);
            let y = j * (box_spc_col) + (j - 1) * (BOX_SIZE);
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
    particles.push(new Particle(box_list[0][0], box_list[0][1], BOX_SIZE, true, 0));

    for (let b = 0; b < box_list.length; b++) {
        for (let i = 0; i < POP_NUM; i++) {
            particles.push(new Particle(box_list[b][0], box_list[b][1], BOX_SIZE, false, b));
        }
    }
}

function setup() {
    let canvas = createCanvas(WIDTH, HEIGHT);
    canvas.parent('simulation');

    input = select('#box-size');
    input.elt.value = BOX_SIZE;

    slider_inf_prob = select('#inf-prob');
    slider_inf_prob.elt.value = INFECTION_PROB / 10;
    slider_inf_prob.elt.min = 0;
    slider_inf_prob.elt.max = 100;
    slider_inf_prob.elt.step = 5;

    slider_inf_radius = select('#inf-radius');
    slider_inf_radius.elt.value = INFECTION_RADIUS;
    slider_inf_radius.elt.min = 0;
    slider_inf_radius.elt.max = 100;
    slider_inf_radius.elt.step = 5;

    slider_inf_days_cure = select('#days-cure');
    slider_inf_days_cure.elt.value = DAYS_CURE;
    slider_inf_days_cure.elt.min = 0;
    slider_inf_days_cure.elt.max = 1000;
    slider_inf_days_cure.elt.step = 50;

    slider_inf_population = select('#pop-box');
    slider_inf_population.elt.value = POP_NUM;
    slider_inf_population.elt.min = 0;
    slider_inf_population.elt.max = 50;
    slider_inf_population.elt.step = 1;

    normallabel = select('#healthy-people');
    infectedlabel = select('#infected-people');
    recoveredlabel = select('#recovered-people');

    button = select('#restart');
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
    let number = input.value();
    if (number === '') {
        number = BOX_SIZE;
    }
    BOX_SIZE = parseInt(number);
    INFECTION_PROB = parseInt(slider_inf_prob.value()) * 10;
    INFECTION_RADIUS = parseInt(slider_inf_radius.value());
    DAYS_CURE = parseInt(slider_inf_days_cure.value());
    POP_NUM = parseInt(slider_inf_population.value());

    console.log('infection', INFECTION_PROB);
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
    // label_slider_inf_prob.html('Probabilidade de contaminação: ' + slider_inf_prob.value());
    slider_inf_prob.elt.labels[0].innerHTML =  'Probabilidade de' +
        ' contaminação: ' + slider_inf_prob.value();
    slider_inf_radius.elt.labels[0].innerHTML =  'Raio de contaminação: ' + slider_inf_radius.value();
    slider_inf_days_cure.elt.labels[0].innerHTML =  'Dias para cura: ' + slider_inf_days_cure.value();
    slider_inf_population.elt.labels[0].innerHTML =  'População por caixa: ' + slider_inf_population.value();

    normallabel.html('Normal: ' + normal);
    infectedlabel.html('Infectados: ' + infected);
    recoveredlabel.html('Recuperados: ' + recovered);
}