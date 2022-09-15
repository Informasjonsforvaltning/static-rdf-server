/// <reference types="cypress" />

describe('ontology specification, language = default', () => {
  it('displays correct title and content', () => {
    cy.visit('http://localhost:8080/specifications/dcat-ap-no')
    cy.title().should('eq', 'Standard for beskrivelse av datasett, datatjenester og datakataloger (DCAT-AP-NO)')
  })
})

describe('ontology specification, language = en-GB', () => {
  it('displays correct title and content', () => {
    cy.visit('http://localhost:8080/specifications/dcat-ap-no', {
      headers: {
        "accept-language": "en-GB,en;q=0.9,nb-NO;q=0.8,nb;q=0.7,en-US;q=0.6,da;q=0.5,no;q=0.4",
      }
    })
    cy.title().should('eq', 'Standard for beskrivelse av datasett, datatjenester og datakataloger (DCAT-AP-NO)')
  })
})


describe('ontology specification, language = nb-NO', () => {
  it('displays correct title and content', () => {
    cy.visit('http://localhost:8080/specifications/dcat-ap-no', {
      headers: {
        "accept-language": "nb-NO,nb;q=0.9,no;q=0.8,en-GB;q=0.7,en;q=0.6,en-US;q=0.5,da;q=0.4",
      }
    })
    cy.title().should('eq', 'Standard for beskrivelse av datasett, datatjenester og datakataloger (DCAT-AP-NO)')
  })
})


describe('ontology specification, language = nn-NO', () => {
  it('displays correct title and content', () => {
    cy.visit('http://localhost:8080/specifications/dcat-ap-no', {
      headers: {
        "accept-language": "nn-NO,nn;q=0.9,no;q=0.8,en-GB;q=0.7,en;q=0.6,en-US;q=0.5,da;q=0.4",
      }
    })
    cy.title().should('eq', 'Standard for beskrivelse av datasett, datatjenester og datakataloger (DCAT-AP-NO)')
  })
})
