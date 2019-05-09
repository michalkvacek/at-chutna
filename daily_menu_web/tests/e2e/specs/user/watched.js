// https://docs.cypress.io/api/introduction/api.html

describe('Test sledování restaurace', () => {
    it('Přidat restauraci do sledovaných', () => {

        cy.login().then(() => {
            cy.visit('/');

            // add restaurants to watched
            cy.get('.restaurant-detail-item').find('.not-watched-restaurant-btn').first().click().then(() => {
                cy.wait(1000);
                cy.visit('/sledovane');
                cy.get('.watched-restaurants-heading').should('contain', 'Sledované');
                cy.get('.watched-restaurants-list').find('.restaurant').its('length').should('be.gte', 1)
            })

        });
    });

    it('Odebrat restauraci ze sledovaných', () => {

        cy.login().then(() => {
            cy.visit('/sledovane');

            // add restaurants to watched
            cy.get('.watched-restaurant-btn').click({multiple: true}).then(() => {
                cy.wait(5000);

                cy.get('.watched-restaurants-list').should('not.exist');

            })

        });
    });
});
