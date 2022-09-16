/// <reference types="cypress" />


describe('ontologies specifications, language = default', () => {
  it('displays correct title and content', () => {
    cy.visit('http://localhost:8080/specifications')
    cy.get('html[lang="en"]').should('exist');
    cy.title().should('eq', 'Specifications')
    cy.get("h2").first().contains("Specifications");
    cy.get('ul').children().should('have.length', 1);
    cy.get('ul li:first').should('to.contain', 'dcat-ap-no')
  })
})

describe('ontologies specifications, language = en-GB', () => {
  it('displays correct title and content in lang en', () => {
    cy.visit('http://localhost:8080/specifications', {
      headers: {
        "accept-language": "en-GB,en;q=0.9,nb-NO;q=0.8,nb;q=0.7,en-US;q=0.6,da;q=0.5,no;q=0.4",
      }
    })
    cy.get('html[lang="en"]').should('exist');
    cy.title().should('eq', 'Specifications')
    cy.get("h2").first().contains("Specifications");
    cy.get('ul').children().should('have.length', 1);
    cy.get('ul li:first').should('to.contain', 'dcat-ap-no')
  })
})


describe('ontologies specifications, language = nb-NO', () => {
  it.skip('displays correct title and content in lang nb', () => {
    cy.visit('http://localhost:8080/specifications', {
      headers: {
        "accept-language": "nb-NO,nb;q=0.9,no;q=0.8,en-GB;q=0.7,en;q=0.6,en-US;q=0.5,da;q=0.4",
      }
    })
    cy.get('html[lang="nb"]').should('exist');
    cy.title().should('eq', 'Specifications')
    cy.get("h2").first().contains("Specifications");
    cy.get('ul').children().should('have.length', 1);
    cy.get('ul li:first').should('to.contain', 'dcat-ap-no')
  })
})


describe('ontologies specifications, language = nn-NO', () => {
  it.skip('displays correct title and content in lang nn', () => {
    cy.visit('http://localhost:8080/specifications', {
      headers: {
        "accept-language": "nn-NO,nn;q=0.9,no;q=0.8,en-GB;q=0.7,en;q=0.6,en-US;q=0.5,da;q=0.4",
      }
    })
    cy.get('html[lang="nn"]').should('exist');
    cy.title().should('eq', 'Specifications')
    cy.get("h2").first().contains("Specifications");
    cy.get('ul').children().should('have.length', 1);
    cy.get('ul li:first').should('to.contain', 'dcat-ap-no')
  })
})
