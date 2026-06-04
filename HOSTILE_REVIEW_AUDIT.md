# Hostile Reviewer Audit

**Paper:** "Institutional Observability Under Scaled AI Governance"
**Date:** June 4, 2026

Three independent hostile reviewers simulated. Each looks for different vulnerabilities.

---

## Reviewer A: The Empiricist

*"I don't care how elegant your model is. Show me data."*

### Major Concerns

**A1. No empirical validation whatsoever.**
This is a simulation paper. The parameters come from one 1997 study. The calibration uses two public reports, not primary data. There is no comparison to real-world oversight outcomes.

**Severity:** 🔴 HIGH
**Defense:** Acknowledged in limitations. Paper is positioned as theoretical groundwork. Empirical validation is future work. But Reviewer A will not be satisfied by this.

**A2. The 2.71x claim is presented as a finding, not a modeling assumption.**
The paper says "human triage pipelines saturate 2.71x faster." This is derived from Kingman's approximation with assumed parameters. It's a mathematical result given the assumptions, not an empirical finding.

**Severity:** 🟠 MEDIUM
**Defense:** The paper states this is from Kingman's heavy-traffic approximation. It's presented as an analytical bound. But the language could be tightened to avoid implying empirical measurement.

**A3. Where are the error bars on the SEDI values?**
Figure 5 shows SEDI as a single line with no uncertainty. SEDI is computed from variance ratios — those variances have sampling error. Where is it?

**Severity:** 🟡 MEDIUM
**Defense:** SEDI is computed analytically from the degradation function, not estimated from data. But a sensitivity analysis would help.

### Verdict: MAJOR REVISION — needs empirical grounding

---

## Reviewer B: The Methodologist

*"Your simulation is fine. Your claims outrun it."*

### Major Concerns

**B1. N_MC = 120 is not justified.**
Why 120? Why not 50? Why not 500? There's no power analysis, no convergence diagnostic. The paper just says "120 runs yield stable 95% CI" without proving it.

**Severity:** 🟠 MEDIUM
**Defense:** 120 is standard for Monte Carlo. CIs are computed. But a convergence plot would help.

**B2. The R² > 0.95 claim is vague.**
R² for what? The fit of the analytical D(rho) to the MC median? Over what range? Is this reported anywhere in the code output?

**Severity:** 🟡 MEDIUM
**Defense:** The code computes the comparison. R² is mentioned in the caption. Could be more explicit.

**B3. KDE bandwidth selection is arbitrary.**
The paper uses bw_method=0.05 for KDE. Why 0.05? Different bandwidths produce different-looking distributions. This matters because the paper's argument depends on the shape of these distributions.

**Severity:** 🟡 LOW
**Defense:** 0.05 is a reasonable default for beta-distributed data on [0,1]. But could be justified.

**B4. The three mechanisms overlap conceptually.**
Mechanism I (assurance surface inflation), Mechanism II (routing fragmentation), and Mechanism III (depth asymmetry) are all consequences of the same throughput asymmetry. They could be one section.

**Severity:** 🟡 LOW
**Defense:** They are distinct failure pathways with different architectural implications. Separate treatment is warranted.

### Verdict: MINOR REVISION — tighten methods justification

---

## Reviewer C: The Gatekeeper

*"This is not what we publish. The author doesn't understand our field."*

### Major Concerns

**C1. The paper reads like a CS workshop paper with governance buzzwords.**
O(N) notation, state-space models, KDE plots, Monte Carlo simulations. This is computer science, not technology-in-society scholarship. Where is the engagement with STS literature? With science and technology studies? With sociological theory beyond one Meyer & Rowan citation?

**Severity:** 🔴 HIGH
**Defense:** The paper's contribution IS the formal modeling of a governance failure mode. It engages with Bovens, Nissenbaum, Eubanks, Lipsky. But Reviewer C wants deeper STS engagement.

**C2. The author is a high school student with no academic affiliation.**
This raises questions about quality control, mentorship, and whether the work meets scholarly standards. Who supervised this? Who verified the math?

**Severity:** 🔴 HIGH (for desk rejection risk)
**Defense:** The work speaks for itself. The code is public. The math is verifiable. But some editors will desk-reject on author credentials alone.

**C3. Citing AAAI workshop papers as references is inappropriate.**
Three of 16 references are from the same 2026 workshop. Workshop papers are not peer-reviewed at journal standard. This looks like citation padding or a citation ring.

**Severity:** 🟠 MEDIUM
**Defense:** The workshop papers are cited substantively as architectural context. They are not foundational references. But Reviewer C has a point.

**C4. The paper claims to derive "governance-by-design principles" but these are just common-sense recommendations.**
"Treat oversight capacity as a scaling constraint" — this is obvious. "Deploy SEDI as a monitoring metric" — this is circular (the paper invents SEDI and then recommends using it). "Separate answerability from enforcement" — Bovens said this in 2007.

**Severity:** 🟡 MEDIUM
**Defense:** The principles are operationalizations of the model's findings. They are specific (naming actors, mechanisms, thresholds), not vague. But the novelty of the principles themselves could be questioned.

### Verdict: DESK REJECT (if editor agrees with framing concerns)

---

## Summary of Vulnerabilities

| # | Vulnerability | Reviewer | Severity | Fixable? |
|---|---|---|---|---|
| 1 | No empirical validation | A | 🔴 HIGH | No (inherent to theoretical paper) |
| 2 | Author is high school student | C | 🔴 HIGH | No (but cover letter addresses it honestly) |
| 3 | CS-heavy writing style | C | 🔴 HIGH | Partially (intro/conclusion rewritten) |
| 4 | 2.71x framed as finding vs. assumption | A | 🟠 MEDIUM | Yes (tighten language) |
| 5 | N_MC=120 not justified | B | 🟠 MEDIUM | Yes (add convergence note) |
| 6 | Workshop paper citations | C | 🟠 MEDIUM | Partially (they're substantive citations) |
| 7 | R² claim vague | B | 🟡 MEDIUM | Yes (make explicit) |
| 8 | SEDI error bars missing | A | 🟡 MEDIUM | Partially (analytical, not empirical) |
| 9 | KDE bandwidth arbitrary | B | 🟡 LOW | Yes (justify) |
| 10 | Mechanisms overlap | B | 🟡 LOW | No (intentional structure) |
| 11 | Governance principles not novel | C | 🟡 LOW | Partially (they're operationalizations) |

---

## Overall Assessment

The paper can survive hostile review. The core mathematical contribution is sound. The code backs the simulation claims. The limitations are honest.

The biggest risks are:
1. An empiricist reviewer who won't accept theoretical work (Reviewer A)
2. An editor who desk-rejects based on author credentials (Reviewer C)
3. The CS/STS stylistic tension that neither audience fully embraces

These are inherent risks of an interdisciplinary theoretical paper from an unusual author. They cannot be fully eliminated — only mitigated through honest framing and public code.
