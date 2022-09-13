/// <reference types="cypress" />

// Welcome to Cypress!
//
// This spec file contains a variety of sample tests
// for a todo list app that are designed to demonstrate
// the power of writing tests in Cypress.
//
// To learn more about how Cypress works and
// what makes it such an awesome testing tool,
// please read our getting started guide:
// https://on.cypress.io/introduction-to-cypress

describe('ontology, language = default', () => {
  beforeEach(() => {
    cy.visit('http://localhost:8080/contract-test/hello-world')
  })

  it('displays correct title', () => {
    cy.title().should('eq', 'Hallo verden')
  })
})

describe('ontology-types language = en-GB', () => {
  beforeEach(() => {
    cy.visit('http://localhost:8080/contract-test/hello-world', {
      headers: {
        "accept-language": "en-GB,en;q=0.9,nb-NO;q=0.8,nb;q=0.7,en-US;q=0.6,da;q=0.5,no;q=0.4",
      }
    })
  })

  it('displays correct title', () => {
    cy.title().should('eq', 'Hello world')
  })
})


describe('ontology-types language = nb-NO', () => {
  beforeEach(() => {
    cy.visit('http://localhost:8080/contract-test/hello-world', {
      headers: {
        "accept-language": "nb-NO,nb;q=0.9,no;q=0.8,en-GB;q=0.7,en;q=0.6,en-US;q=0.5,da;q=0.4",
      }
    })
  })

  it('displays correct title', () => {
    cy.title().should('eq', 'Hallo verden')
  })
})


describe('ontology-types language = nn-NO', () => {
  beforeEach(() => {
    cy.visit('http://localhost:8080/contract-test/hello-world', {
      headers: {
        "accept-language": "nn-NO,nn;q=0.9,no;q=0.8,en-GB;q=0.7,en;q=0.6,en-US;q=0.5,da;q=0.4",
      }
    })
  })

  it('displays correct title', () => {
    cy.title().should('eq', 'Hallo verda')
  })
})
