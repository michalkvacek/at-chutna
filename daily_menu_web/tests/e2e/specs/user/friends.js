// https://docs.cypress.io/api/introduction/api.html

describe('Test seznamu přátel', () => {
    it('Přidání do seznamu', () => {

        cy.login().then(() => {
            cy.visit('/spolecny-obed');

            cy.createRandomUser().then((user) => {
                cy.get('.friend-email').find('input').type(user.email);
                cy.get('#search-friend-form').find('[type=submit]').click();

                cy.get('.friendship-list').find('.friendship').its('length').should('be.gte', 1);
            })


        });
    });

    it('Odebrání ze seznamu', () => {

        cy.login().then(() => {
            cy.visit('/spolecny-obed');


            cy.get('.friendship-list').find('.friendship').its('length').should('be.gte', 1);

            cy.get('.friendship').find('.remove-friend').click({multiple: true, force: true});

            cy.wait(2000);

            cy.get('.friendship-list').find('.friendship').should('not.exist');


        });
    });
});
