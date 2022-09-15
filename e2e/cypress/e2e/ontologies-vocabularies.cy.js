/// <reference types="cypress" />


describe('ontologies vocabularies, language = default', () => {
  it('displays correct title and content', () => {
    cy.visit('http://localhost:8080/vocabularies')
    cy.title().should('eq', 'Vocabularies')
    cy.get("h2").first().contains("Vocabularies");
    cy.get('ul').children().should('have.length', 1);
    cy.get('ul li:first').should('to.contain', 'audience-type')
  })
})

describe('ontologies vocabularies, language = en-GB', () => {
  it('displays correct title and content', () => {
    cy.visit('http://localhost:8080/vocabularies', {
      headers: {
        "accept-language": "en-GB,en;q=0.9,nb-NO;q=0.8,nb;q=0.7,en-US;q=0.6,da;q=0.5,no;q=0.4",
      }
    })
    cy.title().should('eq', 'Vocabularies')
    cy.get("h2").first().contains("Vocabularies");
    cy.get('ul').children().should('have.length', 1);
    cy.get('ul li:first').should('to.contain', 'audience-type')
  })
})


describe('ontologies vocabularies, language = nb-NO', () => {
  it('displays correct title and content', () => {
    cy.visit('http://localhost:8080/vocabularies', {
      headers: {
        "accept-language": "nb-NO,nb;q=0.9,no;q=0.8,en-GB;q=0.7,en;q=0.6,en-US;q=0.5,da;q=0.4",
      }
    })
    cy.title().should('eq', 'Vocabularies')
    cy.get("h2").first().contains("Vocabularies");
    cy.get('ul').children().should('have.length', 1);
    cy.get('ul li:first').should('to.contain', 'audience-type')
  })
})


describe('ontologies vocabularies, language = nn-NO', () => {
  it('displays correct title and content', () => {
    cy.visit('http://localhost:8080/vocabularies', {
      headers: {
        "accept-language": "nn-NO,nn;q=0.9,no;q=0.8,en-GB;q=0.7,en;q=0.6,en-US;q=0.5,da;q=0.4",
      }
    })
    cy.title().should('eq', 'Vocabularies')
    cy.get("h2").first().contains("Vocabularies");
    cy.get('ul').children().should('have.length', 1);
    cy.get('ul li:first').should('to.contain', 'audience-type')
  })
})
