# Flows

Several flows together: in a reply, or saved as one file. Follow Multiple flows and Saving to a file in `SKILL.md`.

Both share one legend at the start, listing every shape used across all the flows. In a reply:

```
Auth flows for a recipe app.
(shared legend block)

**1. Login**: returning user signs in.
(mermaid block)

**2. Signup**: new user creates an account.
(mermaid block)
```

In a saved file, the shared legend sits under the `#` title, and each flow gets a numbered `##` heading and one short line instead of the bold line. Link the flows with `sub` nodes named after each other, so a reader can follow one into the next.

Below the line is a complete saved file, `auth.md`, exactly as it should be written.

---

# Auth

```mermaid
flowchart TD
  lgTerminator@{ shape: stadium, label: "Terminator: start or end" }
  lgDisplay@{ shape: curv-trap, label: "Display: screen or page" }
  lgProcess@{ shape: rect, label: "Process: step or action" }
  lgDecision@{ shape: diam, label: "Decision: yes or no question" }
  lgManualInput@{ shape: sl-rect, label: "Manual Input: user enters data" }
  lgManualOperation@{ shape: trap-t, label: "Manual Operation: user acts outside the app" }
  lgPredefinedProcess@{ shape: fr-rect, label: "Predefined Process: subflow or other flow" }
  lgPreparation@{ shape: hex, label: "Preparation: setup before a step" }
  lgDocument@{ shape: doc, label: "Document: email, receipt or file" }
  lgMultipleDocuments@{ shape: docs, label: "Multiple Documents: several documents" }
  lgMerge@{ shape: flip-tri, label: "Merge: two paths rejoin" }

  lgTerminator ~~~ lgDecision
  lgDisplay ~~~ lgManualInput
  lgProcess ~~~ lgManualOperation
  lgDecision ~~~ lgPredefinedProcess
  lgManualInput ~~~ lgPreparation
  lgManualOperation ~~~ lgDocument
  lgPredefinedProcess ~~~ lgMultipleDocuments
  lgPreparation ~~~ lgMerge
```

## 1. Login

Returning user signs in with email and password.

```mermaid
flowchart TD
  startLogin@{ shape: stadium, label: "Opens login" }
  scrLogin@{ shape: curv-trap, label: "Login screen" }
  inCredentials@{ shape: sl-rect, label: "Enters email and password" }
  decValid@{ shape: diam, label: "Credentials valid?" }
  scrError@{ shape: curv-trap, label: "Inline error" }
  subSignup@{ shape: fr-rect, label: "Signup flow" }
  exitHome@{ shape: stadium, label: "Lands on home" }

  startLogin --> scrLogin
  scrLogin -->|Sign in| inCredentials
  scrLogin -->|Sign up| subSignup
  inCredentials --> decValid
  decValid -->|Yes| exitHome
  decValid -->|No| scrError
  scrError --> inCredentials
```

## 2. Signup

New user creates an account and verifies their email.

```mermaid
flowchart TD
  startSignup@{ shape: stadium, label: "Taps Sign up" }
  scrSignup@{ shape: curv-trap, label: "Sign up screen" }
  inDetails@{ shape: sl-rect, label: "Enters name, email, password" }
  decRegistered@{ shape: diam, label: "Email already registered?" }
  subLogin@{ shape: fr-rect, label: "Login flow" }
  docVerify@{ shape: doc, label: "Verification email" }
  manOpenEmail@{ shape: trap-t, label: "Opens email app" }
  actTapLink@{ shape: rect, label: "Taps verify link" }
  subFirstTime@{ shape: fr-rect, label: "First-time user flow" }

  startSignup --> scrSignup
  scrSignup --> inDetails
  inDetails --> decRegistered
  decRegistered -->|Yes| subLogin
  decRegistered -->|No| docVerify
  docVerify --> manOpenEmail
  manOpenEmail --> actTapLink
  actTapLink --> subFirstTime
```

## 3. First-time user

Verified user sets up their profile and lands on a home that isn't empty.

```mermaid
flowchart TD
  startVerified@{ shape: stadium, label: "Email verified" }
  scrWelcome@{ shape: curv-trap, label: "Welcome screen" }
  inProfile@{ shape: sl-rect, label: "Adds name and photo" }
  decInvite@{ shape: diam, label: "Invites teammates?" }
  inEmails@{ shape: sl-rect, label: "Enters teammate emails" }
  mdocInvites@{ shape: docs, label: "Invite emails" }
  mergeInvite@{ shape: flip-tri, label: " " }
  prepSample@{ shape: hex, label: "Sets up sample project" }
  exitHome@{ shape: stadium, label: "Lands on home" }

  startVerified --> scrWelcome
  scrWelcome --> inProfile
  inProfile --> decInvite
  decInvite -->|Yes| inEmails
  decInvite -->|No| mergeInvite
  inEmails --> mdocInvites
  mdocInvites --> mergeInvite
  mergeInvite --> prepSample
  prepSample --> exitHome
```
