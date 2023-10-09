$cupList = $('#cupcake-list');
$formDiv = $('#form-div')
let cupcakes;
let attributes = ['flavor', 'size', 'rating', 'image'];
async function start(){
    resp = await axios.get('/api/cupcakes');

    cupcakes = resp.data.cupcakes;

    for (let cupcake of cupcakes){
        $cupList.append(`<li>${cupcake.flavor}</li>`);
    }
    createForm()
}

async function createForm(){
    $formDiv.append("<form id='form'></form>")
    $form = $('#form');
    
    for (let attribute of attributes){
        $form.append(`<label for='${attribute}'>${attribute}:</label>`);
        $form.append(`<input id='${attribute}' name='${attribute}'>`);
    }
    $form.append(`<button type='submit' id='submit'>SUBMIT</button>`);
    $('#submit').on('click', formHandler);
}
start();

async function formHandler(evt){
    evt.preventDefault();

    $flavor = $('#flavor');
    $size = $('#size');
    $rating = $('#rating');
    $image = $('#image');
    $cupList.append(`<li>${$flavor.val()}</li>`);

    let data = {
        flavor: $flavor.val(),
        size: $size.val(),
        rating: $rating.val(),
        image: $image.val()
    }

    resp = await axios.post(`/api/cupcakes`, data);
    console.log(resp);

    $flavor.val('');
    $size.val('');
    $rating.val('');
    $image.val('');


}