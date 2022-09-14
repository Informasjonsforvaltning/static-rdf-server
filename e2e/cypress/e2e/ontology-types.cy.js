/// <reference types="cypress" />


describe('ontology-types, language = default', () => {
  beforeEach(() => {
    cy.visit('http://localhost:8080/')
  })

  it('displays correct title', () => {
    cy.title().should('eq', 'Ontologi-typer')
  })
})

describe('ontology-types language = en-GB', () => {
  beforeEach(() => {
    cy.visit('http://localhost:8080/', {
      headers: {
        "accept-language": "en-GB,en;q=0.9,nb-NO;q=0.8,nb;q=0.7,en-US;q=0.6,da;q=0.5,no;q=0.4",
      }
    })
  })

  // Not implemented yet
  it.skip('displays correct title', () => {
    cy.title().should('eq', 'Ontology types')
  })
})


describe('ontology-types language = nb-NO', () => {
  beforeEach(() => {
    cy.visit('http://localhost:8080/', {
      headers: {
        "accept-language": "nb-NO,nb;q=0.9,no;q=0.8,en-GB;q=0.7,en;q=0.6,en-US;q=0.5,da;q=0.4",
      }
    })
  })

  it('displays correct title', () => {
    cy.title().should('eq', 'Ontologi-typer')
  })
})


describe('ontology-types language = nn-NO', () => {
  beforeEach(() => {
    cy.visit('http://localhost:8080/', {
      headers: {
        "accept-language": "nn-NO,nn;q=0.9,no;q=0.8,en-GB;q=0.7,en;q=0.6,en-US;q=0.5,da;q=0.4",
      }
    })
  })

  // Not implemented yet
  it.skip('displays correct title', () => {
    cy.title().should('eq', 'Ontologi-typar')
  })
})
