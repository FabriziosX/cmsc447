var r = document.querySelector(':root');

function Add_Student_On() {
    r.style.setProperty('--ADDer', 'flex');
    r.style.setProperty('--ADDNone', 'all');
}
function Add_Student_OFF() {
    r.style.setProperty('--ADDer', 'none');
    r.style.setProperty('--ADDNone', 'none');
}

function Edit_Student_On() {
    r.style.setProperty('--EDitor', 'flex');
    r.style.setProperty('--EditNone', 'all');
    
}

function Edit_Student_OFF() {
    r.style.setProperty('--EDitor', 'none');
    r.style.setProperty('--EditNone', 'none');
}