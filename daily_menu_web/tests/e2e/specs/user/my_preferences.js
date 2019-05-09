// https://docs.cypress.io/api/introduction/api.html

describe('Test nastavování preferencí uživatele', () => {
    it('Přidat preferenci', () => {

        cy.login().then(() => {
            cy.visit('/me-chute');

            cy.get('.preference-list-select').click().then(($select) => {
                cy.contains('Ryby').click(() => {
                    cy.get('.preference-list-item')
                        .its('length')
                        .should('be.gt', 0);
                });
            });

            cy.get('.preference-list-item').contains('Mám rád/a').click().then(() => {
                cy.get('.preference-list-item').contains('Odebrat').click().then(() => {
                    cy.get('.preference-list-item')
                        .should('have.length', 0)
                })
            });
        });
    });
});
