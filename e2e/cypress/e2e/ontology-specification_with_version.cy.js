/// <reference types="cypress" />

describe('ontology specification with version, language = default', () => {
  it('displays correct title and content', () => {
    cy.visit('http://localhost:8080/specifications/dcat-ap-no/v1.1')
    cy.get('html[lang="nb"]').should('exist');
    cy.title().should('eq', 'Standard for beskrivelse av datasett og datakataloger (DCAT-AP-NO)')
  })
})

describe('ontology specification with version, language = en-GB', () => {
  it('should fall back to default (lang = nb)', () => {
    cy.visit('http://localhost:8080/specifications/dcat-ap-no/v1.1', {
      headers: {
        "accept-language": "en-GB,en;q=0.9,nb-NO;q=0.8,nb;q=0.7,en-US;q=0.6,da;q=0.5,no;q=0.4",
      }
    })
    cy.get('html[lang="nb"]').should('exist');
    cy.title().should('eq', 'Standard for beskrivelse av datasett og datakataloger (DCAT-AP-NO)')
  })
})


describe('ontology specification with version, language = nb-NO', () => {
  it('displays correct title and content', () => {
    cy.visit('http://localhost:8080/specifications/dcat-ap-no/v1.1', {
      headers: {
        "accept-language": "nb-NO,nb;q=0.9,no;q=0.8,en-GB;q=0.7,en;q=0.6,en-US;q=0.5,da;q=0.4",
      }
    })
    cy.get('html[lang="nb"]').should('exist');
    cy.title().should('eq', 'Standard for beskrivelse av datasett og datakataloger (DCAT-AP-NO)')
  })
})


describe('ontology specification with version, language = nn-NO', () => {
  it('should fall back to default (lang=nb"', () => {
    cy.visit('http://localhost:8080/specifications/dcat-ap-no/v1.1', {
      headers: {
        "accept-language": "nn-NO,nn;q=0.9,no;q=0.8,en-GB;q=0.7,en;q=0.6,en-US;q=0.5,da;q=0.4",
      }
    })
    cy.get('html[lang="nb"]').should('exist');
    cy.title().should('eq', 'Standard for beskrivelse av datasett og datakataloger (DCAT-AP-NO)')
  })
})
