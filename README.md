# End-to-End Retail Credit Risk Analytics & IND-AS 109 Provisioning Engine

An enterprise-grade credit risk modeling and analytics pipeline built to evaluate loan-level retail portfolios within the Indian banking and NBFC regulatory framework. This project simulates credit policy underwriting, tracks cohort delinquency, trains a Probability of Default (PD) machine learning model, estimates IND-AS 109 Expected Credit Loss (ECL), and serves dynamic portfolio insights via an interactive executive dashboard.

---

## Executive Summary

| Project Pillar | Technical Implementation | Business & Regulatory Outcome |
| :--- | :--- | :--- |
| **Approval Engine** | Hard cut-off policy filtering ($\text{CIBIL} \ge 650$, $\text{DTI} \le 55\%$) | Automates top-of-funnel application approval decisions [cite: End-to-end Credit Risk Analytics: Build a project using loan-level data to calculate approval rates, delinquency, PD, expected loss, vintage performance and risk segmentation, then create an executive dashboard.] |
| **Risk Segmentation** | 4-tier CIBIL bracket mapping (*Prime Plus*, *Prime*, *Near Prime*, *Sub-Prime*) | Isolates high-risk cohorts and tracks non-performing asset (NPA) rates |
| **Vintage & Roll Rates** | Cohort performance tracking & $4 \times 4$ delinquency transition matrices | Monitors account migration across IND-AS 109 stages (Stage 1 to Stage 3) |
| **PD & ECL Engine** | Logistic Regression ($12\text{-month default}$) combined with product-specific LGDs | Computes $ECL = PD \times LGD \times EAD$ for regulatory provisioning |
| **Executive Dashboard** | Streamlit & Plotly interactive monitoring layer | Enables real-time strategy simulation and stress-testing for Risk Leads |

---
Technical Workflow & Analytical Framework
1. Credit Policy Engine & Risk Segmentation
   * Policy Underwriting: Evaluates incoming loan applications against standard retail banking rules: CIBIL threshold ($\ge 650$), Debt-to-Income cap ($\le 55\%$), and minimum income constraints.
   * Portfolio Segmentation: Booked accounts are mapped to risk tiers (Prime Plus, Prime, Near Prime, Sub-Prime) to monitor risk concentration.
2. Vintage Curves & Roll Rate Matrices
   * Vintage Cohorts: Calculates cumulative default rates ($90+$ Days Past Due) grouped by origination month to detect portfolio degradation over time.
   * Roll Rates (Transition Matrices): Measures account movement between delinquency buckets:
                                                                                           Stage 1 (0–30 DPD): Performing exposure
                                                                                           Stage 2 (31–90 DPD): Significant Increase in Credit Risk (SICR)
                                                                                           Stage 3 (90+ DPD): Default / Non-Performing Asset (NPA)
3. Probability of Default (PD) & IND-AS 109 Provisioning
   * PD Modeling: Logistic Regression model trained on key risk drivers (cibil_score, dti_ratio, monthly_income_inr, loan_amount_inr) with class-weight balancing.
   * Loss Given Default (LGD): Product-differentiated parameters:
                                                               Personal Loans (Unsecured): $65\%$ LGD
                                                               Two-Wheeler Loans (Secured/Repossessable): $45\%$ LGD
                                                               Consumer Durables: $55\%$ LGD
   * Expected Credit Loss Framework: Account-level regulatory provisioning via:

                                                                         $$\text{ECL} = \text{PD} \times \text{LGD} \times \text{EAD}$$

## streamlit run dashboard/app.py
