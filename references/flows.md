# Flows

Several flows together: in a reply, or saved as one file. Follow Multiple flows and Saving to a file in `SKILL.md`.

Both share one legend at the start, listing every shape used across all the flows. In a reply:

```
Onboarding flows for a recipe app.
(shared legend block)

**1. App launch**: routes first-time and returning users.
(mermaid block)

**2. Welcome**: intro, then Create account or Log in.
(mermaid block)
```

In a saved file, the shared legend sits under the `#` title, and each flow gets a numbered `##` heading and one short line instead of the bold line. Link the flows with `sub` nodes named after each other, so a reader can follow one into the next.

Below the line is a complete saved file, `onboarding.md`, exactly as it should be written. It covers everything from first launch to the home screen in 6 linked flows. The note in Password reset is there to show the syntax; add notes only when the user asks.

---

# Onboarding

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
  lgDelay@{ shape: delay, label: "Delay: waiting" }
  lgDatabase@{ shape: cyl, label: "Database: saved records" }
  lgInternalStorage@{ shape: win-pane, label: "Internal Storage: session or cache" }
  lgDocument@{ shape: doc, label: "Document: email, receipt or file" }
  lgMerge@{ shape: flip-tri, label: "Merge: two paths rejoin" }
  lgCurlyBraceNote@{ shape: brace, label: "Curly Brace Note: comment on a node" }

  lgTerminator ~~~ lgDecision
  lgDisplay ~~~ lgManualInput
  lgProcess ~~~ lgManualOperation
  lgDecision ~~~ lgPredefinedProcess
  lgManualInput ~~~ lgPreparation
  lgManualOperation ~~~ lgDelay
  lgPredefinedProcess ~~~ lgDatabase
  lgPreparation ~~~ lgInternalStorage
  lgDelay ~~~ lgDocument
  lgDatabase ~~~ lgMerge
  lgInternalStorage ~~~ lgCurlyBraceNote
```

## 1. App launch

Every launch: first-time users go to Welcome, returning users go home or log in.

```mermaid
flowchart TD
  startLaunch@{ shape: stadium, label: "Opens the app" }
  scrSplash@{ shape: curv-trap, label: "Splash screen" }
  memSession@{ shape: win-pane, label: "Saved session" }
  decFirst@{ shape: diam, label: "First launch?" }
  decSession@{ shape: diam, label: "Session still valid?" }
  subWelcome@{ shape: fr-rect, label: "Welcome flow" }
  subLogin@{ shape: fr-rect, label: "Login flow" }
  exitHome@{ shape: stadium, label: "Lands on home" }

  startLaunch --> scrSplash
  scrSplash --> memSession
  memSession --> decFirst
  decFirst -->|Yes| subWelcome
  decFirst -->|No| decSession
  decSession -->|Yes| exitHome
  decSession -->|No| subLogin
```

## 2. Welcome

First-time user sees the intro, then picks Create account or Log in.

```mermaid
flowchart TD
  startWelcome@{ shape: stadium, label: "First launch" }
  scrIntro@{ shape: curv-trap, label: "Intro screens" }
  decSkip@{ shape: diam, label: "Skips the intro?" }
  actSwipe@{ shape: rect, label: "Swipes through intro" }
  mergeIntro@{ shape: flip-tri, label: " " }
  scrWelcome@{ shape: curv-trap, label: "Welcome screen" }
  subSignup@{ shape: fr-rect, label: "Signup flow" }
  subLogin@{ shape: fr-rect, label: "Login flow" }

  startWelcome --> scrIntro
  scrIntro --> decSkip
  decSkip -->|No| actSwipe
  decSkip -->|Yes| mergeIntro
  actSwipe --> mergeIntro
  mergeIntro --> scrWelcome
  scrWelcome -->|Create account| subSignup
  scrWelcome -->|Log in| subLogin
```

## 3. Signup

New user signs up with email and verifies it, or continues with Google or Apple.

```mermaid
flowchart TD
  startSignup@{ shape: stadium, label: "Taps Create account" }
  scrSignup@{ shape: curv-trap, label: "Sign up screen" }
  inDetails@{ shape: sl-rect, label: "Enters name, email, password" }
  decRegistered@{ shape: diam, label: "Email already registered?" }
  scrExists@{ shape: curv-trap, label: "Account exists message" }
  decRules@{ shape: diam, label: "Password meets rules?" }
  scrRules@{ shape: curv-trap, label: "Password rules hint" }
  dbUser@{ shape: cyl, label: "New user record" }
  docVerify@{ shape: doc, label: "Verification email" }
  manOpenEmail@{ shape: trap-t, label: "Opens email app" }
  decLink@{ shape: diam, label: "Link still valid?" }
  scrExpired@{ shape: curv-trap, label: "Link expired screen" }
  actResend@{ shape: rect, label: "Taps Resend email" }
  manSocial@{ shape: trap-t, label: "Picks Google or Apple account" }
  decSocialDone@{ shape: diam, label: "Sign in completed?" }
  decSocialKnown@{ shape: diam, label: "Account already exists?" }
  dbSocialUser@{ shape: cyl, label: "New social user record" }
  subLogin@{ shape: fr-rect, label: "Login flow" }
  subFirstTime@{ shape: fr-rect, label: "First-time user flow" }

  startSignup --> scrSignup
  scrSignup -->|Email| inDetails
  scrSignup -->|Google or Apple| manSocial
  inDetails --> decRegistered
  decRegistered -->|Yes| scrExists
  decRegistered -->|No| decRules
  scrExists --> subLogin
  decRules -->|No| scrRules
  decRules -->|Yes| dbUser
  scrRules --> inDetails
  dbUser --> docVerify
  docVerify --> manOpenEmail
  manOpenEmail --> decLink
  decLink -->|Yes| subFirstTime
  decLink -->|No| scrExpired
  scrExpired --> actResend
  actResend --> docVerify
  manSocial --> decSocialDone
  decSocialDone -->|No| scrSignup
  decSocialDone -->|Yes| decSocialKnown
  decSocialKnown -->|Yes| subLogin
  decSocialKnown -->|No| dbSocialUser
  dbSocialUser --> subFirstTime
```

## 4. Login

Returning user logs in with email or Google or Apple, with wrong password and lockout branches.

```mermaid
flowchart TD
  startLogin@{ shape: stadium, label: "Taps Log in" }
  scrLogin@{ shape: curv-trap, label: "Login screen" }
  inCredentials@{ shape: sl-rect, label: "Enters email and password" }
  decValid@{ shape: diam, label: "Credentials valid?" }
  decAttempts@{ shape: diam, label: "Under 5 attempts?" }
  scrError@{ shape: curv-trap, label: "Inline error" }
  scrLocked@{ shape: curv-trap, label: "Account locked screen" }
  manSocial@{ shape: trap-t, label: "Picks Google or Apple account" }
  decSocialDone@{ shape: diam, label: "Sign in completed?" }
  decSocialKnown@{ shape: diam, label: "Account exists?" }
  memSession@{ shape: win-pane, label: "New session" }
  subReset@{ shape: fr-rect, label: "Password reset flow" }
  subSignup@{ shape: fr-rect, label: "Signup flow" }
  exitHome@{ shape: stadium, label: "Lands on home" }

  startLogin --> scrLogin
  scrLogin -->|Email| inCredentials
  scrLogin -->|Google or Apple| manSocial
  scrLogin -->|Forgot password| subReset
  scrLogin -->|Create account| subSignup
  inCredentials --> decValid
  decValid -->|Yes| memSession
  decValid -->|No| decAttempts
  decAttempts -->|Yes| scrError
  decAttempts -->|No| scrLocked
  scrError --> inCredentials
  scrLocked --> subReset
  manSocial --> decSocialDone
  decSocialDone -->|No| scrLogin
  decSocialDone -->|Yes| decSocialKnown
  decSocialKnown -->|Yes| memSession
  decSocialKnown -->|No| subSignup
  memSession --> exitHome
```

## 5. Password reset

User resets a forgotten password by email link. A note marks that the same message shows whether or not the email is registered.

```mermaid
flowchart TD
  startForgot@{ shape: stadium, label: "Taps Forgot password" }
  scrForgot@{ shape: curv-trap, label: "Forgot password screen" }
  inEmail@{ shape: sl-rect, label: "Enters email" }
  actSend@{ shape: rect, label: "Taps Send link" }
  decKnown@{ shape: diam, label: "Email registered?" }
  docReset@{ shape: doc, label: "Reset email" }
  scrCheck@{ shape: curv-trap, label: "Check your email screen" }
  noteSame@{ shape: brace, label: "Same message for every email" }
  waitEmail@{ shape: delay, label: "Waits for email" }
  manOpenEmail@{ shape: trap-t, label: "Opens email app" }
  decLink@{ shape: diam, label: "Link still valid?" }
  scrExpired@{ shape: curv-trap, label: "Link expired screen" }
  scrNewPassword@{ shape: curv-trap, label: "New password screen" }
  inNewPassword@{ shape: sl-rect, label: "Enters new password" }
  decRules@{ shape: diam, label: "Meets password rules?" }
  scrRules@{ shape: curv-trap, label: "Password rules hint" }
  dbUser@{ shape: cyl, label: "Updated user record" }
  exitHome@{ shape: stadium, label: "Lands on home" }

  startForgot --> scrForgot
  scrForgot --> inEmail
  inEmail --> actSend
  actSend --> decKnown
  decKnown -->|Yes| docReset
  decKnown -->|No| scrCheck
  noteSame -.- scrCheck
  docReset --> scrCheck
  scrCheck --> waitEmail
  waitEmail --> manOpenEmail
  manOpenEmail --> decLink
  decLink -->|No| scrExpired
  decLink -->|Yes| scrNewPassword
  scrExpired --> scrForgot
  scrNewPassword --> inNewPassword
  inNewPassword --> decRules
  decRules -->|No| scrRules
  decRules -->|Yes| dbUser
  scrRules --> inNewPassword
  dbUser --> exitHome
```

## 6. First-time user

New user sets up their profile and notifications, then lands on a home that isn't empty.

```mermaid
flowchart TD
  startNew@{ shape: stadium, label: "Account created" }
  scrHello@{ shape: curv-trap, label: "Getting started screen" }
  inProfile@{ shape: sl-rect, label: "Adds name and photo" }
  scrPermission@{ shape: curv-trap, label: "Notification prompt" }
  decAllow@{ shape: diam, label: "Allows notifications?" }
  actRegister@{ shape: rect, label: "Registers device for push" }
  mergePush@{ shape: flip-tri, label: " " }
  inInterests@{ shape: sl-rect, label: "Picks interests" }
  prepSample@{ shape: hex, label: "Sets up sample content" }
  exitHome@{ shape: stadium, label: "Lands on home" }

  startNew --> scrHello
  scrHello --> inProfile
  inProfile --> scrPermission
  scrPermission --> decAllow
  decAllow -->|Yes| actRegister
  decAllow -->|No| mergePush
  actRegister --> mergePush
  mergePush --> inInterests
  inInterests --> prepSample
  prepSample --> exitHome
```
