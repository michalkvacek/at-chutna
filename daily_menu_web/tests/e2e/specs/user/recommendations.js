// https://docs.cypress.io/api/introduction/api.html

describe('Doporučení', () => {
    it('Existence doporučení na homepage', () => {

        cy.login().then(() => {
            cy.visit('/');

            cy.contains('Dnes doporučujeme').should('exist');
        });
    });
});
