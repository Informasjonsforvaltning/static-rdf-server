/// <reference types="cypress" />

describe('ontology vocabulary, language = default', () => {
  it('displays correct title and content', () => {
    cy.visit('http://localhost:8080/vocabularies/audience-type')
    cy.get('html[lang="nb"]').should('exist');
    cy.title().should('eq', 'audience-type')
  })
})

describe('ontology vocabulary, language = en-GB', () => {
  it('displays correct title and content', () => {
    cy.visit('http://localhost:8080/vocabularies/audience-type', {
      headers: {
        "accept-language": "en-GB,en;q=0.9,nb-NO;q=0.8,nb;q=0.7,en-US;q=0.6,da;q=0.5,no;q=0.4",
      }
    })
    cy.get('html[lang="en"]').should('exist');
    cy.title().should('eq', 'audience-type')
  })
})


describe('ontology vocabulary, language = nb-NO', () => {
  it('displays correct title and content', () => {
    cy.visit('http://localhost:8080/vocabularies/audience-type', {
      headers: {
        "accept-language": "nb-NO,nb;q=0.9,no;q=0.8,en-GB;q=0.7,en;q=0.6,en-US;q=0.5,da;q=0.4",
      }
    })
    cy.get('html[lang="nb"]').should('exist');
    cy.title().should('eq', 'audience-type')
  })
})


describe('ontology vocabulary, language = nn-NO', () => {
  it('displays correct title and content', () => {
    cy.visit('http://localhost:8080/vocabularies/audience-type', {
      headers: {
        "accept-language": "nn-NO,nn;q=0.9,no;q=0.8,en-GB;q=0.7,en;q=0.6,en-US;q=0.5,da;q=0.4",
      }
    })
    cy.get('html[lang="nn"]').should('exist');
    cy.title().should('eq', 'audience-type')
  })
})
