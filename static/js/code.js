// The orders (up to down) of lines matter a lot!
//1.html, 11.html
const erase = document.querySelector(".erase");
const eraselabel = document.querySelector('label[for="erase"]');
erase.onmouseover = () => {
    eraselabel.innerHTML = "Recommended on public or shared devices.";
}
erase.onmouseout = () => { 
    eraselabel.innerHTML = "all input.";
}

// 2.html, 3.html: count down be4 redirect. class name in common.
let countdown = 20;
setInterval(() => { // no execution without appointed tag/class/id.
    document.querySelector('.countdown').innerHTML = 
    `Redirect after ${countdown} seconds`;
    countdown -= 1;
    if (countdown == -1) { location.href = '/loggingin';}
}, 1000);

// if each one login session is limited to 5 min, then n = 300.
let n = 300;
setInterval(() => {
    n -= 1;
    document.querySelector('header h2').innerHTML = 
    `Auto Logout after ${n} seconds.`;
    if (n == -1) { location.href = "/";}
}, 1000);

//1.html: wish num, keyed-in data saved in different ways.
let numStorage = sessionStorage.getItem("now_num");
let dateStorage = sessionStorage.getItem("pickup_date");
let wishStorage = localStorage.getItem("wish");
document.addEventListener('DOMContentLoaded', () => {
    
    const wish = document.getElementById("wish_num");
    const check = document.querySelector('#yes');
    const num = document.getElementById("now_num");
    const date = document.querySelector("#pickup_date");
    const label = document.querySelector('[for="yesbox"]');

    if (numStorage != null) { num.value = numStorage;}
    if (dateStorage != null) { date.value = dateStorage;}
    if (wishStorage != null && wishStorage > 0) {
        wish.value = wishStorage;
        check.checked = true;
        check.setAttribute("disabled", "disabled");
        label.innerHTML = "Fixed";
    }
    else { 
        wish.value = 1; // autofulfilled.
        check.checked = false;
        label.innerHTML = "Fix number on this device.";
        check.removeAttribute("disabled");
    }

    num.onchange = () => { sessionStorage.setItem("now_num", num.value);}
    date.onchange = () => { sessionStorage.setItem("pickup_date", date.value);}
    wish.onchange = () => {
        check.removeAttribute("disabled");
        check.checked = false;
        label.innerHTML = "Fix number on this device.";
        localStorage.clear();
    }
    check.onchange = () => {
        check.setAttribute("disabled", "disabled");
        localStorage.setItem("wish", wish.value);
        label.innerHTML = "Fixed";
    }
// erase input concerning preorder on page 1.html.
    erase.onclick = () => {
        sessionStorage.clear();
        date.value = "";
        num.value = "";
    }
})

//11.html: keyed-in data saved in session. Remember me.
let timeStorage = sessionStorage.getItem("pktime");
let contactStorage = sessionStorage.getItem("contact");
let phoneStorage = sessionStorage.getItem("phone");
let titleStorage = sessionStorage.getItem("title");
document.addEventListener('DOMContentLoaded', () => {

    const pickup_time = document.querySelector("#pickup_time");
    const contact = document.querySelector("#contact");
    const phone = document.querySelector("#phone");
    const title = document.querySelector("#title");
    const RM = document.querySelector("#RememberMe");

    if (timeStorage != null) { pickup_time.value = timeStorage;}
    if (contactStorage != null) { 
        contact.value = contactStorage;
        RM.checked = true;
        RM.setAttribute("disabled", "disabled");
    }
    if (phoneStorage != null) { phone.value = phoneStorage;}
    if (titleStorage != null) { title.value = titleStorage;}

    pickup_time.onchange = () => { sessionStorage.setItem("pktime", pickup_time.value);}
    contact.onchange = () => { 
        RM.removeAttribute("disabled");
        RM.checked = false;
        sessionStorage.clear();
    }
    phone.onchange = () => { 
        RM.removeAttribute("disabled");
        RM.checked = false;
        sessionStorage.clear();
    }
    title.onchange = () => { 
        RM.removeAttribute("disabled");
        RM.checked = false;
        sessionStorage.clear();
    }
    RM.onchange = () => {
        sessionStorage.setItem("contact", contact.value);
        sessionStorage.setItem("phone", phone.value);
        sessionStorage.setItem("title", title.value);
        RM.checked = true;
        RM.setAttribute("disabled", "disabled");
    }

// back to the page where to make or revoke wishes is possible.
    document.querySelector("#back").onclick = () => {
        location.href = '/loggingin';
    }
// show alert onmouseover alone.
    const warningsign = document.querySelector("#warningsign");
    warningsign.onmouseover = () => {
        warningsign.innerHTML = " (Not recommended on public or shared devices.)";
    }
    warningsign.onmouseout = () => {
        warningsign.innerHTML = '&#9888';
    }
// erase all input on page 11.html.
    erase.onclick = () => {
        sessionStorage.clear();
        pickup_time.value = "";
        contact.value = "";
        phone.value = "";
        title.value = "";
        RM.checked = false;
        RM.removeAttribute("disabled");
    }
})


