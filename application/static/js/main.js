// Auto remember the previous data function
let sign_in = document.querySelector("#sign-in");
let password = document.querySelector("#password");
let filter = document.querySelector("#filter")

document.querySelector("#btnFilter").addEventListener("click", () => {

    let data = {
        "sign_in": sign_in.value,
        "password": password.value,
        "filter": filter.value
    }

    fetch("/filter-data", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    })

});

// remember function
let remember_sign_in = () => {
    localStorage.setItem("last_sign_in", sign_in.value);
}
let remember_password = () => {
    localStorage.setItem("last_password", password.value);
}
// auto fill
sign_in.addEventListener("input", remember_sign_in);
password.addEventListener("input", remember_password);
sign_in.addEventListener("change", remember_sign_in);
password.addEventListener("change", remember_password);

// generate the account function when generate button is clicked
document.querySelector("#generate").addEventListener("click", () => {
     // get to local storage
     sign_in.value = localStorage.getItem("last_sign_in");
     password.value = localStorage.getItem("last_password");
})


