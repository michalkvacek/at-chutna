// https://docs.cypress.io/api/introduction/api.html

describe('Test hodnocení menu', () => {
    it('Označení menu', () => {

        cy.login().then(() => {
            cy.visit('/');

            cy.get('.restaurants-with-menu-list')
                .find('.restaurant-detail-item').first()
                .find('.daily-menu-rating').should('exist');

            cy.get('.restaurants-with-menu-list')
                .find('.restaurant-detail-item').first()
                .find('[aria-label=Ohodnotit]').first().click({force: true, multiple: true});

            cy.contains('Chutnalo mi').click({force: true});

            cy.get('.restaurants-with-menu-list')
                .find('.restaurant-detail-item').first().should('contain', 'Díky za reakci');


        });
    });


});
