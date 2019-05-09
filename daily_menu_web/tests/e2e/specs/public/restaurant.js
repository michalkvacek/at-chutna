// https://docs.cypress.io/api/introduction/api.html

describe('Test detailu restaurace', () => {
    it('Zobrazení první dostupné restaurace', () => {
        cy.visit('/');

        cy.get('.restaurants-with-menu-list')
            .find('.restaurant-detail-item')
            .find('.restaurant-detail-link').first().click();

        cy.location('pathname').should('contain', 'restaurace')


    })
});
