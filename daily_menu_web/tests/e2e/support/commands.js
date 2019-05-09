// ***********************************************
// This example commands.js shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************
//
//
// -- This is a parent command --
Cypress.Commands.add("login", () => {
    let API_URL = Cypress.env('api_url');
    let user = Cypress.env('user');
    let password = Cypress.env('password');

    cy.request({
        url: API_URL + "login/",
        method: "POST",
        body: {
            username: user,
            password: password
        }
    }).then(({body}) => {

        window.localStorage.setItem('authorizationToken', body.token);

        return body
    })
});


Cypress.Commands.add("createRandomUser", () => {
    let API_URL = Cypress.env('api_url');

    let email = "cypress-" + Math.random() + "@example.com";
    let password = "test" + Math.random();

    return cy.request({
        url: API_URL + "registration/",
        method: "POST",
        body: {
            email: email,
            username: email,
            first_name: '',
            last_name: '',
            password: password
        }
    }).then(({body}) => {
        return body
    })
});

