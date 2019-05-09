// https://docs.cypress.io/api/introduction/api.html

describe('Test registrace', () => {
    it('Vytvoření uživatele', () => {
        cy.visit('/registrace');
        cy.clearLocalStorage();

        let email = "cypress-" + Math.random() + "@example.com";
        let password = "test"+Math.random();

        cy.get('.register-email').find('input').type(email);
        cy.get('.register-password').find('input').type(password);

        // login after registation
        cy.get('[type=submit]').click().then(() => {
            cy.location('pathname').should('eq', '/me-chute');
        })
    });

});
