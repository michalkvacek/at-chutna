// https://docs.cypress.io/api/introduction/api.html

describe('Test přihlášení', () => {
    it('Přihlášení uživatele - špatné heslo', () => {
        cy.visit('/prihlaseni');
        cy.clearLocalStorage();

        let password = "spatneheslo";

        cy.get('.login-email').find('input').type(Cypress.env('user'));
        cy.get('.login-password').find('input').type(`${password}{enter}`);

        cy.get('#login-form')
            .find('.error')
            .its('length')
            .should('be.gte', 0);
    });

    it('Přihlášení uživatele - správné heslo', () => {
        cy.visit('/prihlaseni');
        cy.clearLocalStorage();

        let password = Cypress.env('password');

        cy.get('.login-email').find('input').type(Cypress.env('user'));
        cy.get('.login-password').find('input').type(`${password}{enter}`);
        cy.get('[type=submit]').click().then(() => {

            cy.wait(2000);

            cy.location('pathname').should('eq', '/me-chute');

            expect(localStorage.getItem('authorizationToken')).to.not.equal(null)
        })
    })
});
