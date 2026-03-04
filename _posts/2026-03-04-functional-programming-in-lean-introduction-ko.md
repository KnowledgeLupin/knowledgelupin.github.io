---
title: "Functional Programming in Lean: Introduction (한국어 번역)"
date: 2026-03-04 15:00:00 +0900
categories: [Programming, Lean]
tags: [Lean, Functional Programming, Translation]
toc: true
math: false
author: KnowledgeLupin
---

> 원문: [Functional Programming in Lean - Introduction](https://lean-lang.org/functional_programming_in_lean/Introduction/)  
> 저자: David Thrane Christiansen  
> 라이선스: [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/)  
> 이 글은 학습 목적으로 작성한 비공식 한국어 번역입니다.
{: .prompt-info }

# Functional Programming in Lean 소개

Lean은 종속 타입 이론(dependent type theory)에 기반한 상호작용 정리 증명기입니다. 처음에는 Microsoft Research에서 개발되었고, 현재는 [Lean FRO](https://lean-fro.org)에서 개발이 진행됩니다. 종속 타입 이론은 프로그램과 증명의 세계를 하나로 연결하므로, Lean은 정리 증명기이면서 동시에 프로그래밍 언어이기도 합니다. Lean은 이 이중적 성격을 진지하게 반영하며, 범용 프로그래밍 언어로 사용할 수 있도록 설계되었습니다. 실제로 Lean 자체도 Lean으로 구현되어 있습니다. 이 책은 Lean으로 프로그램을 작성하는 방법을 다룹니다.

프로그래밍 언어 관점에서 Lean은 종속 타입을 갖춘 strict한 순수 함수형 언어입니다. Lean 프로그래밍을 배우는 과정의 큰 부분은 이 특성들이 프로그램 작성 방식에 어떤 영향을 주는지, 그리고 함수형 프로그래머처럼 사고하는 법을 익히는 데 있습니다. strict하다는 것은 함수 호출 시 대부분의 언어처럼 함수 본문 실행 전에 인자가 먼저 완전히 계산된다는 뜻입니다.

순수성(purity)은 프로그램의 타입에 명시되지 않은 부수 효과를 허용하지 않는다는 뜻입니다. 예를 들어 메모리 위치를 수정하거나, 이메일을 보내거나, 파일을 삭제하는 동작은 타입이 이를 드러내지 않으면 수행할 수 없습니다. 또한 Lean이 함수형 언어라는 말은 함수가 다른 값들처럼 일급 값(first-class value)이며, 실행 모델이 수학적 식의 평가 방식에서 영감을 받았다는 의미입니다.

Lean의 가장 독특한 특징인 종속 타입은 타입을 언어의 일급 요소로 다룹니다. 이로 인해 타입 안에 프로그램이 들어갈 수 있고, 프로그램이 타입을 계산할 수도 있습니다.

이 책은 Lean을 배우고 싶은 프로그래머를 대상으로 하지만, 독자가 함수형 프로그래밍 언어를 이미 사용해 봤다고 가정하지는 않습니다. Haskell, OCaml, F# 같은 언어 경험은 필수가 아닙니다. 다만 반복문, 함수, 자료구조처럼 대부분의 프로그래밍 언어에서 공통으로 쓰이는 개념은 알고 있다고 가정합니다. 따라서 이 책은 함수형 프로그래밍의 입문서로는 좋지만, 프로그래밍 일반의 첫 입문서로는 적합하지 않습니다.

Lean을 증명 보조기로 사용하는 수학자도 결국 맞춤형 증명 자동화 도구를 작성해야 할 때가 많습니다. 이 책은 그런 독자도 대상으로 합니다. 자동화 도구가 복잡해질수록 함수형 언어의 프로그램에 가까워지지만, 많은 수학자들은 주로 Python이나 Mathematica에 익숙합니다. 이 책은 그 간극을 메워, 더 많은 수학자가 유지보수 가능하고 이해하기 쉬운 증명 자동화 도구를 작성하도록 돕습니다.

이 책은 처음부터 끝까지 순서대로 읽도록 구성되어 있습니다. 개념은 한 번에 하나씩 도입되며, 뒤쪽 내용은 앞에서 배운 내용을 알고 있다고 가정합니다. 어떤 주제는 앞에서 간단히 언급한 뒤 뒤 장에서 더 깊게 다루기도 합니다. 일부 절에는 연습문제가 포함되어 있는데, 이해를 굳히는 데 도움이 되므로 풀어보는 것을 권합니다. 또한 읽는 동안 Lean을 직접 탐구하며 배운 내용을 창의적으로 활용해 보는 것도 유익합니다.

## 핵심 개념 정리

### 1. 종속 타입 이론 (`dependent type theory`)
Lean의 이론적 바탕은 "타입이 값에 의존할 수 있다"는 아이디어입니다. 즉 프로그램과 증명을 같은 언어 안에서 다루며, 타입을 통해 명세를 더 정밀하게 표현합니다. 이 덕분에 실행 전에 많은 오류를 제거할 수 있습니다.

```lean
inductive Vec (α : Type u) : Nat -> Type u where
  | nil  : Vec α 0
  | cons : α -> Vec α n -> Vec α (n + 1)

def head : Vec α (n + 1) -> α
  | .cons x _ => x
```

### 2. 함수형 프로그래밍 (`functional programming`)
함수형 프로그래밍은 상태 변경보다 함수 조합으로 문제를 푸는 방식입니다. 무엇을 반복해서 바꾸는지보다 데이터를 어떻게 변환할지 선언적으로 표현합니다.

```lean
def squareAll (xs : List Nat) : List Nat :=
  xs.map (fun x => x * x)

#eval squareAll [1, 2, 3, 4]
```

### 3. 상호작용 정리 증명기 (`interactive theorem prover`)
Lean은 증명을 자동으로 대신 해주는 도구라기보다, 사람이 증명 단계를 제시하면 기계가 각 단계를 엄밀하게 검증해 주는 도구입니다. 목표를 하나씩 줄여 가며 증명을 완성하는 상호작용 방식이 핵심입니다.

```lean
theorem and_comm (P Q : Prop) : P ∧ Q -> Q ∧ P := by
  intro h
  exact And.intro h.right h.left
```

### 4. 순수 함수형 언어 (`purity`)
순수성은 함수가 타입에 드러나지 않은 부수 효과를 몰래 수행하지 않는다는 뜻입니다. 효과가 필요한 연산은 `IO`처럼 타입으로 분리되어 코드의 의미가 더 명확해집니다.

```lean
def add (a b : Nat) : Nat := a + b

def greet : IO Unit := do
  IO.println "Hello, Lean!"
```

### 5. strict 평가 전략 (`strict evaluation`)
Lean은 기본적으로 함수 인자를 먼저 계산한 뒤 함수 본문을 실행하는 strict 평가 전략을 따릅니다. 따라서 인자를 실제로 쓰지 않더라도 계산 비용이 먼저 발생할 수 있습니다. 필요하면 thunk(함수로 감싼 지연 계산) 패턴으로 제어할 수 있습니다.

```lean
def ignoreThunk (_x : Unit -> Nat) : Nat := 1
```

### 6. 종속 타입 (`dependent types`)
종속 타입은 값이 타입에 들어가는 기능 자체를 가리킵니다. 예를 들어 인덱스의 범위 조건을 타입으로 강제하면, 런타임 오류 대신 컴파일 단계에서 안전성을 확보할 수 있습니다.

```lean
def pick (xs : List α) (i : Fin xs.length) : α :=
  xs.get i

#eval pick [10, 20, 30] ⟨1, by decide⟩
```

### 7. `type class` / `applicative functor` / `monad`
이 세 가지는 Lean에서 추상화와 효과 조합을 이해하는 핵심 축입니다.

- `type class`: 공통 인터페이스 기반 다형성
- `applicative functor`: 서로 독립적인 효과 계산의 결합
- `monad`: 앞 단계 결과에 의존하는 순차 계산의 결합

```lean
def mkUser (name : String) (age : Nat) : String :=
  s!"{name}({age})"

#eval mkUser <$> some "Kim" <*> some 30
#eval mkUser <$> some "Kim" <*> (none : Option Nat)

def parseNat? (s : String) : Option Nat := s.toNat?
def halfIfEven (n : Nat) : Option Nat :=
  if n % 2 == 0 then some (n / 2) else none

def pipeline (s : String) : Option Nat := do
  let n <- parseNat? s
  halfIfEven n
```

## Lean 시작하기

Lean으로 프로그램을 작성하고 실행하기 전에, 먼저 자신의 컴퓨터에 Lean 개발 환경을 설정해야 합니다. Lean 도구 체인은 다음 요소로 구성됩니다.

- `elan`: `rustup`, `ghcup`처럼 Lean 컴파일러 toolchain을 관리합니다.
- `lake`: `cargo`, `make`, Gradle처럼 Lean 패키지와 의존성을 빌드합니다.
- `lean`: 개별 Lean 파일을 타입 검사하고 컴파일하며, 작성 중인 파일에 대한 정보를 프로그래머 도구에 제공합니다. 보통 사용자가 직접 호출하기보다 다른 도구를 통해 실행됩니다.
- Visual Studio Code, Emacs 같은 에디터 플러그인: `lean`과 통신하여 정보를 편리하게 보여줍니다.

설치 방법의 최신 정보는 [Lean manual](https://lean-lang.org/lean4/doc/quickstart.html)을 참고하세요.

## 표기 관례

Lean에 입력하는 코드 예시는 다음과 같은 형식으로 제시됩니다.

```lean
def add1 (n : Nat) : Nat := n + 1
#eval add1 7
```

위 예시의 마지막 줄(`#eval`)은 Lean에게 값을 계산하라고 지시하는 명령입니다. Lean의 출력은 보통 다음과 같이 표시됩니다.

```text
8
```

Lean의 오류 메시지는 다음과 같은 형식으로 표시됩니다.

```text
Application type mismatch: The argument
  "seven"
has type
  String
but is expected to have type
  Nat
in the application
  add1 "seven"
```

경고 메시지는 다음과 같이 표시됩니다.

```text
declaration uses 'sorry'
```

## Unicode 입력

관용적인 Lean 코드는 ASCII에 포함되지 않는 다양한 Unicode 문자를 사용합니다. 예를 들어 그리스 문자 `α`, `β`, 그리고 화살표 `→`는 이 책의 첫 장에서도 등장합니다. 이런 표기 덕분에 Lean 코드는 일반적인 수학 표기와 더 비슷해집니다.

기본 설정에서는 Visual Studio Code와 Emacs 모두 백슬래시(`\`)와 이름을 조합해 문자를 입력할 수 있습니다. 예를 들어 `\alpha`를 입력하면 `α`가 됩니다. Visual Studio Code에서는 해당 문자 위에 마우스를 올려 tooltip으로 입력 방법을 확인할 수 있고, Emacs에서는 커서를 문자 위에 둔 뒤 `C-c C-k`를 사용하면 됩니다.

## 릴리스 히스토리

### 2025년 10월

책이 최신 안정 Lean 버전(4.23.0)에 맞춰 업데이트되었고, functional induction과 `grind` tactic 설명이 추가되었습니다.

### 2025년 8월

책의 코드 복사/붙여넣기 관련 문제를 해결한 유지보수 릴리스입니다.

### 2025년 7월

Lean 4.21 버전에 맞춰 업데이트되었습니다.

### 2025년 6월

책이 Verso로 재포맷되었습니다.

### 2025년 4월

내용이 대폭 갱신되었고 Lean 4.18을 설명하도록 변경되었습니다.

### 2024년 1월

예제 프로그램의 회귀(regression)를 수정한 소규모 버그 수정 릴리스입니다.

### 2023년 10월

첫 유지보수 릴리스로, 여러 작은 문제를 고치고 Lean 최신 릴리스에 맞춰 본문을 갱신했습니다.

### 2023년 5월

책이 완성되었습니다. 2023년 4월 사전 릴리스 대비 세부 사항이 개선되고 작은 오류가 수정되었습니다.

### 2023년 4월

tactic을 이용한 증명 인터루드와 마지막 장이 추가되었습니다. 마지막 장은 성능/비용 모델과 종료성 및 프로그램 동치 증명을 함께 다룹니다. 이 릴리스는 최종 릴리스 직전 마지막 릴리스입니다.

### 2023년 3월

종속 타입과 인덱스드 패밀리(indexed families)로 프로그래밍하는 장이 추가되었습니다.

### 2023년 1월

`do`-notation에서 사용할 수 있는 명령형 기능 설명을 포함한 monad transformer 장이 추가되었습니다.

### 2022년 12월

applicative functor 장이 추가되었고, 구조체와 type class 설명이 더 자세해졌습니다. monad 설명도 함께 개선되었습니다. 2022년 12월 릴리스는 겨울 휴일로 인해 2023년 1월로 연기되었습니다.

### 2022년 11월

monad 프로그래밍 장이 추가되었고, coercion 절의 JSON 예제가 전체 코드를 포함하도록 업데이트되었습니다.

### 2022년 10월

type class 장이 완성되었습니다. 또한 type class 장 바로 앞에 명제, 증명, tactic을 소개하는 짧은 인터루드가 추가되었습니다. 표준 라이브러리 type class 일부를 이해하는 데 이 배경이 도움이 됩니다.

### 2022년 9월

연산자 오버로딩 메커니즘이자 코드 조직의 핵심 수단인 Lean type class 장의 전반부가 추가되었습니다. 또한 Lean stream API 변경을 반영해 2장이 업데이트되었습니다.

### 2022년 8월

세 번째 공개 릴리스로, 프로그램 컴파일/실행과 Lean의 부수 효과 모델을 다루는 2장이 추가되었습니다.

### 2022년 7월

두 번째 공개 릴리스에서 1장이 완성되었습니다.

### 2022년 6월

첫 공개 릴리스로, 소개와 1장 일부로 구성되었습니다.

## 저자 소개

David Thrane Christiansen은 20년간 함수형 언어를, 10년간 종속 타입을 사용해 왔습니다. Daniel P. Friedman과 함께 종속 타입 이론의 핵심 아이디어를 소개하는 입문서 [The Little Typer](https://thelittletyper.com)를 집필했습니다. 코펜하겐 IT University에서 박사 학위를 받았고, 학위 과정 중에는 Idris 언어의 첫 버전에 주요 기여자로 활동했습니다.

학계를 떠난 뒤에는 미국 오리건주 포틀랜드의 Galois, 덴마크 코펜하겐의 Deon Digital에서 소프트웨어 개발자로 일했으며, Haskell Foundation의 Executive Director를 맡았습니다. 이 책 집필 시점에는 [Lean Focused Research Organization](https://lean-fro.org)에서 Lean 전담 개발자로 근무하고 있습니다.

## 라이선스

이 저작물은 [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/)에 따라 배포됩니다.

책의 원본 버전은 David Thrane Christiansen이 Microsoft Corporation과의 계약을 통해 작성했으며, Microsoft는 이를 CC BY 4.0으로 공개했습니다. 현재 버전은 Lean의 최신 변화에 맞추기 위해 저자가 원본을 수정한 버전입니다. 자세한 변경 내역은 책의 [source code repository](https://github.com/leanprover/fp-lean)에서 확인할 수 있습니다.
