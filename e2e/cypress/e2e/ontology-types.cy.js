/// <reference types="cypress" />


describe('ontology-types, language = default', () => {
  it('displays correct title and content', () => {
    cy.visit('http://localhost:8080/')
    cy.get('html[lang="nb"]').should('exist');
    cy.title().should('eq', 'Ontologi-typer')
    cy.get("h2").first().contains("Typer");
    cy.get('ul').children().should('have.length', 3);
    cy.get('ul li:first').should('to.contain', 'contract-test')
    cy.get('ul li:nth-child(2)').should('to.contain', 'specifications')
    cy.get('ul li:nth-child(3)').should('to.contain', 'vocabularies')
  })
})

describe('ontology-types, language = en-GB', () => {
  it.skip('displays correct title and content', () => {
    cy.visit('http://localhost:8080/', {
      headers: {
        "accept-language": "en-GB,en;q=0.9,nb-NO;q=0.8,nb;q=0.7,en-US;q=0.6,da;q=0.5,no;q=0.4",
      }
    })
    cy.title().should('eq', 'Ontology types')
  })
})


describe('ontology-types, language = nb-NO', () => {
  it('displays correct title and content', () => {
    cy.visit('http://localhost:8080/', {
      headers: {
        "accept-language": "nb-NO,nb;q=0.9,no;q=0.8,en-GB;q=0.7,en;q=0.6,en-US;q=0.5,da;q=0.4",
      }
    })
    cy.visit('http://localhost:8080/')
    cy.get('html[lang="nb"]').should('exist');
    cy.title().should('eq', 'Ontologi-typer')
    cy.get("h2").first().contains("Typer");
    cy.get('ul').children().should('have.length', 3);
    cy.get('ul li:first').should('to.contain', 'contract-test')
    cy.get('ul li:nth-child(2)').should('to.contain', 'specifications')
    cy.get('ul li:nth-child(3)').should('to.contain', 'vocabularies')
  })
})


describe('ontology-types, language = nn-NO', () => {
  // Not implemented yet
  it.skip('displays correct title and content', () => {
    cy.visit('http://localhost:8080/', {
      headers: {
        "accept-language": "nn-NO,nn;q=0.9,no;q=0.8,en-GB;q=0.7,en;q=0.6,en-US;q=0.5,da;q=0.4",
      }
    })
    cy.title().should('eq', 'Ontologi-typar')
  })
})
