// https://docs.cypress.io/api/introduction/api.html

describe('Test úvodní stránky', () => {
    it('Test výpisu restaurací', () => {
        cy.visit('/');
        cy.contains('h2', 'Dnešní menu');

        cy.get('.restaurants-with-menu-list')
            .find('.restaurant-detail-item')
            .its('length')
            .should('be.gte', 0)
    })
});
