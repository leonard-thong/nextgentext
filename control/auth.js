const signInForm = document.querySelector("#sign_in_form");

if (signInForm) {
    signInForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const email = signInForm["email"].value;
        const password = signInForm["password"].value;

        // var cred = await auth.signInWithEmailAndPassword(email, password);
        // console.log(cred);
        auth.signInWithEmailAndPassword(email, password).then((cred) => {
            console.log(cred.user.uid);
            localStorage.setItem("userid", cred.user.uid);
            url = window.location.origin + "/view/authenticated/dashboard.html";
            window.location.replace(url);
        });
    });
}

const signUpForm = document.querySelector("#sign_up_form");

if (signUpForm) {
    signUpForm.addEventListener("submit", (e) => {
        e.preventDefault();

        const email = signUpForm["email"].value;
        const password = signUpForm["password"].value;

        auth.createUserWithEmailAndPassword(email, password).then((cred) => {
            console.log(cred.user.uid);
            localStorage.setItem("userid", cred.user.uid);
        });
    });
}

const logOutButton = document.querySelector("#logout_button");

if (logOutButton) {
    logOutButton.addEventListener("click", (e) => {
        e.preventDefault();
        auth.signOut().then(() => {
            url = window.location.origin + "/view/unauthenticated/login.html";
            window.location.replace(url);
            localStorage.setItem("userid", "");
        });
    });
}
