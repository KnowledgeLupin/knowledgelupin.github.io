---
title: "Getting to Know Lean (한국어 번역)"
date: 2026-03-04 09:02:00 +0900
categories: [Programming, Lean]
tags: [Lean, Functional Programming, Translation, fp-lean, editor, evaluation, basics]
toc: true
math: false
author: KnowledgeLupin
---


> 원문: [Functional Programming in Lean](https://lean-lang.org/functional_programming_in_lean/Getting-to-Know-Lean/)  
> 저자: David Thrane Christiansen  
> 라이선스: [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/)  
> 이 글은 학습 목적으로 작성한 비공식 한국어 번역이며, 장말 해설이 추가되었습니다.
{: .prompt-info }

# Getting to Know Lean

전통에 따르면 프로그래밍 언어는 콘솔에 `"Hello, world!"`을 표시하는 프로그램을 컴파일하고 실행하여 도입되어야 합니다. 
 이 간단한 프로그램은 언어 도구가 올바르게 설치되었는지 확인하고 프로그래머가 컴파일된 코드를 실행할 수 있는지 확인합니다.

그러나 1970년대부터 프로그래밍이 바뀌었습니다. 
 오늘날 컴파일러는 일반적으로 텍스트 편집기에 통합되며 프로그래밍 환경은 프로그램이 작성될 때 피드백을 제공합니다. 
 Lean도 예외는 아닙니다. Lean은 텍스트 편집기와 통신하고 사용자가 입력할 때 피드백을 제공할 수 있는 확장 버전의 언어 서버 프로토콜을 구현합니다.

Python, Haskell 및 JavaScript와 같은 다양한 언어는 대화형 최상위 레벨 또는 브라우저 콘솔이라고도 알려진 REPL(read-eval-print-loop)을 제공하며 여기에 표현식이나 명령문을 입력할 수 있습니다. 
 그런 다음 언어는 사용자 입력의 결과를 계산하고 표시합니다. 
 반면에 Lean은 이러한 기능을 편집기와의 상호 작용에 통합하여 텍스트 편집기가 프로그램 텍스트 자체에 통합된 피드백을 표시하도록 하는 명령을 제공합니다. 
 이 장에서는 편집기에서 Lean과 상호 작용하는 방법에 대해 간략하게 소개하고 Hello, World! 배치 모드의 명령줄에서 전통적으로 Lean을 사용하는 방법을 설명합니다.

편집기에서 Lean을 열고 각 예를 따라 입력하면서 이 책을 읽는 것이 가장 좋습니다. 
 예제를 가지고 놀면서 무슨 일이 일어나는지 살펴보세요!

Lean을 배우는 프로그래머로서 이해해야 할 가장 중요한 것은 평가가 어떻게 작동하는지입니다. 
 평가는 산술에서와 마찬가지로 표현식의 값을 찾는 과정입니다. 
 예를 들어, $`15 - 6`의 값은 $`9`이고 $`2 × (3 + 1)`의 값은 $`8`입니다. 
 후자 표현식의 값을 찾으려면 $`3 + 1`를 먼저 $`4`로 대체하여 $`2 × 4`을 생성하고 이 값 자체를 $`8`로 줄일 수 있습니다. 
 때로는 수학 표현식에 변수가 포함됩니다. 즉, $`x`의 값이 무엇인지 알 때까지 $`x + 1`의 값을 계산할 수 없습니다. 
 Lean에서 프로그램은 무엇보다도 표현이며, 계산에 대해 생각하는 주요 방법은 표현식을 평가하여 해당 값을 찾는 것입니다.

대부분의 프로그래밍 언어는 _명령형_입니다. 여기서 프로그램은 프로그램의 결과를 찾기 위해 수행해야 하는 일련의 명령문으로 구성됩니다. 
 프로그램은 가변 메모리에 액세스할 수 있으므로 변수가 참조하는 값은 시간이 지남에 따라 변경될 수 있습니다. 
 변경 가능한 상태 외에도 프로그램에는 파일 삭제, 나가는 네트워크 연결 설정, 
 예외 던지기 또는 잡기, 데이터베이스에서 데이터 읽기 등의 다른 부작용이 있을 수 있습니다. 
 "부작용"은 본질적으로 수학적 표현을 평가하는 모델을 따르지 않는 프로그램에서 발생할 수 있는 일을 설명하는 포괄적인 용어입니다.

그러나 Lean에서는 프로그램이 수학적 표현과 동일한 방식으로 작동합니다. 
 일단 값이 주어지면 변수를 다시 할당할 수 없습니다. 표현식 평가에는 부작용이 있을 수 없습니다. 
 두 표현식의 값이 동일한 경우 하나를 다른 표현식으로 바꿔도 프로그램이 다른 결과를 계산하지 않습니다. 
 이는 Lean을 사용하여 콘솔에 `Hello, world!`을 쓸 수 없다는 의미는 아니지만 I/O 수행은 동일한 방식으로 Lean을 사용하는 경험의 핵심 부분이 아닙니다. 
 따라서 이 장에서는 Lean을 사용하여 대화식으로 표현식을 평가하는 방법에 중점을 두고 다음 장에서는 `Hello, world!` 프로그램을 작성, 컴파일 및 실행하는 방법을 설명합니다.

Lean에게 표현식을 평가하도록 요청하려면 편집기에서 표현식 앞에 `#eval`을 쓰면 결과가 다시 보고됩니다. 
 일반적으로 결과는 `#eval` 위에 커서나 마우스 포인터를 놓으면 검색됩니다. 
 예를 들어,

```lean
#eval 1 + 2
```

값을 산출합니다

```text
3
```

Lean은 
 산술 연산자에 대한 우선순위 및 연관성의 일반적인 규칙을 따릅니다. 즉,

```lean
#eval 1 + 2 * 5
```

`15` 대신 `11` 값을 생성합니다.

일반적인 수학적 표기법과 대부분의 프로그래밍 언어는 함수를 인수에 적용하기 위해 괄호(예: `f(x)`)를 사용하지만 Lean은 단순히 인수 옆에 함수를 작성합니다(예: `f x`). 
 함수 적용은 가장 일반적인 작업 중 하나이므로 간결하게 유지하는 것이 좋습니다. 
 글을 쓰는 것보다

```
#eval String.append("Hello, ", "Lean!")
```

`"Hello, Lean!"`을 계산하려면 대신 다음과 같이 작성합니다.

```lean
#eval String.append "Hello, " "Lean!"
```

여기서 함수의 두 인수는 단순히 공백을 사용하여 옆에 작성됩니다.

`(1 + 2) * 5` 표현식의 산술적 요구 괄호에 대한 연산 순서 규칙과 마찬가지로 함수의 인수가 다른 함수 호출을 통해 계산되는 경우에도 괄호가 필요합니다. 
 예를 들어 다음에는 괄호가 필요합니다.

```lean
#eval String.append "great " (String.append "oak " "tree")
```

그렇지 않으면 두 번째 `String.append`은 `"oak "` 및 `"tree"`을 인수로 전달되는 함수가 아니라 첫 번째 인수로 해석되기 때문입니다. 
 내부 `String.append` 호출의 값을 먼저 찾아야 하며 그 후에 `"great "`에 추가하여 최종 값 `"great oak tree"`을 생성할 수 있습니다.

명령형 언어에는 종종 두 가지 종류의 조건이 있습니다. 즉, 부울 값을 기반으로 수행할 명령을 결정하는 조건부 _statement_와 부울 값을 기반으로 두 표현식 중 어느 것을 평가할지 결정하는 조건부 _expression_입니다. 
 예를 들어, C 및 C++에서 조건문은 `if` 및 `else`을 사용하여 작성되는 반면, 조건식은 `?` 및 `:`이 조건을 분기와 구분하는 삼항 연산자로 작성됩니다. 
 Python에서 조건문은 `if`로 시작하는 반면, 조건식은 `if`을 중간에 넣습니다. 
 Lean은 표현식 중심 함수형 언어이므로 조건문은 없고 조건식만 있습니다. 
 `if`, `then` 및 `else`을 사용하여 작성됩니다. 
 예를 들어,

```lean
String.append "it is " (if 1 > 2 then "yes" else "no")
```

평가하다

```lean
String.append "it is " (if false then "yes" else "no")
```

이는 다음과 같이 평가됩니다.

```lean
String.append "it is " "no"
```

최종적으로 `"it is no"`로 평가됩니다.

간결함을 위해 이와 같은 일련의 평가 단계는 때때로 그 사이에 화살표를 사용하여 작성됩니다.

```lean
String.append "it is " (if 1 > 2 then "yes" else "no")
===>
String.append "it is " (if false then "yes" else "no")
===>
String.append "it is " "no"
===>
"it is no"
```

### 자주 만나는 메시지

인수가 누락된 함수 응용 프로그램을 Lean에게 평가하도록 요청하면 오류 메시지가 표시됩니다. 
 특히, 예

```lean
#eval String.append "it is "
```

꽤 긴 오류 메시지가 나타납니다.

```text
could not synthesize a `ToExpr`, `Repr`, or `ToString` instance for type
  String → String
```

이 메시지는 해당 인수 중 일부에만 적용된 Lean 함수가 나머지 인수를 기다리는 새 함수를 반환하기 때문에 발생합니다. 
 Lean은 사용자에게 기능을 표시할 수 없으므로 요청하면 오류를 반환합니다.

### 연습문제

다음 표현식의 값은 무엇입니까? 손으로 작업한 후 
 그런 다음 Lean에 입력하여 작업을 확인하세요.

* `42 + 19` 
 * `String.append "A" (String.append "B" "C")` 
 * `String.append (String.append "A" "B") "C"` 
 * `if 3 == 3 then 5 else 7` 
 * `if 3 == 4 then "equal" else "not equal"`

타입은 
 계산할 수 있는 값을 기준으로 프로그램을 분류합니다. 타입은 프로그램에서 다양한 역할을 수행합니다.

1. 이를 통해 컴파일러는 값의 메모리 내 표현에 대해 결정을 내릴 수 있습니다.

2. 함수의 입력 및 출력에 대한 경량 사양 역할을 하여 프로그래머가 자신의 의도를 다른 사람에게 전달하는 데 도움이 됩니다. 
 컴파일러는 프로그램이 이 사양을 준수하는지 확인합니다.

3. 문자열에 숫자를 추가하는 등의 다양한 잠재적 실수를 방지하여 프로그램에 필요한 테스트 횟수를 줄입니다.

4. Lean 컴파일러가 상용구를 저장할 수 있는 보조 코드 생성을 자동화하는 데 도움이 됩니다.

Lean의 타입 시스템은 유별나게 표현력이 뛰어납니다. 
 타입은 "이 정렬 함수는 입력의 순열을 반환합니다"와 같은 강력한 사양과 "이 함수는 인수 값에 따라 다른 반환 타입을 갖습니다"와 같은 유연한 사양을 인코딩할 수 있습니다. 
 타입 시스템은 수학 정리를 증명하기 위한 본격적인 논리로 사용될 수도 있습니다. 
 이러한 최첨단 표현력이 단순한 타입을 불필요하게 만드는 것은 아니며 이러한 간단한 타입을 이해하는 것이 고급 기능을 사용하기 위한 전제 조건입니다.

Lean의 모든 프로그램에는 타입이 있어야 합니다. 특히 모든 
 표현식은 평가되기 전에 타입이 있어야 합니다. 지금까지의 
 예제에서 Lean은 스스로 타입을 발견할 수 있었지만 
 때로는 타입을 제공해야 할 때도 있습니다. 이는 괄호 안에 콜론 
 연산자를 사용하여 수행됩니다.

```lean
#eval (1 + 2 : Nat)
```

여기서 `Nat`은 임의 정밀도 부호 없는 정수인 _자연수_의 타입입니다. 
 Lean에서 `Nat`은 음수가 아닌 정수 리터럴의 기본 타입입니다. 
 이 기본 타입이 항상 최선의 선택은 아닙니다. 
 C에서 부호 없는 정수는 뺄셈이 0보다 작은 결과를 산출할 때 표현 가능한 가장 큰 숫자로 언더플로우됩니다. 그러나 
 `Nat`은 임의의 큰 부호 없는 숫자를 나타낼 수 있으므로 언더플로할 가장 큰 숫자는 없습니다. 
 따라서 `Nat`에 대한 뺄셈은 그렇지 않은 경우 답이 음수일 경우 `zero`를 반환합니다. 
 예를 들어,

```lean
#eval (1 - 2 : Nat)
```

`-1`이 아닌 `0`로 평가됩니다. 
 음의 정수를 나타낼 수 있는 타입을 사용하려면 직접 제공하십시오.

```lean
#eval (1 - 2 : Int)
```

이 타입을 사용하면 결과는 예상대로 `-1`입니다.

표현식을 평가하지 않고 타입을 확인하려면 `#eval` 대신 `#check`을 사용하십시오. 예를 들어:

```lean
#check (1 - 2 : Int)
```

실제로 빼기를 수행하지 않고 `1 - 2 : Int`을(를) 보고합니다.

프로그램에 타입을 지정할 수 없으면 `#check` 및 `#eval` 모두에서 오류가 반환됩니다. 예를 들어:

```lean
#check String.append ["hello", " "] "world"
```

출력

```text
Application type mismatch: The argument
  ["hello", " "]
has type
  List String
but is expected to have type
  String
in the application
  String.append ["hello", " "]
```

`String.append`에 대한 첫 번째 인수는 문자열이어야 하는데 대신 문자열 목록이 제공되었기 때문입니다.

Lean에서는 `def` 키워드를 사용하여 정의가 도입됩니다. 
 예를 들어, `hello`이라는 이름이 `"Hello"` 문자열을 참조하도록 정의하려면 다음과 같이 작성하십시오.

```lean
def hello := "Hello"
```

Lean에서는 `=` 대신 콜론 등호 연산자 `:=`을 사용하여 새 이름을 정의합니다. 
 `=`는 기존 표현식 간의 동등성을 설명하는 데 사용되며, 서로 다른 두 연산자를 사용하면 혼동을 방지하는 데 도움이 되기 때문입니다.

`hello` 정의에서 `"Hello"` 표현식은 Lean이 정의 타입을 자동으로 결정할 수 있을 만큼 간단합니다. 
 그러나 대부분의 정의는 그렇게 간단하지 않으므로 일반적으로 타입을 추가해야 합니다. 
 이는 정의되는 이름 뒤에 콜론을 사용하여 수행됩니다.

```lean
def lean : String := "Lean"
```

이제 이름이 정의되었으므로 사용할 수 있습니다.

```lean
#eval String.append hello (String.append " " lean)
```

출력

```text
"Hello Lean"
```

Lean에서는 정의된 이름은 정의 후에만 사용할 수 있습니다.

많은 언어에서 함수 정의는 다른 값 정의와 다른 구문을 사용합니다. 
 예를 들어, Python 함수 정의는 `def` 키워드로 시작하고 다른 정의는 등호로 정의됩니다. 
 Lean에서 함수는 다른 값과 동일한 `def` 키워드를 사용하여 정의됩니다. 
 그럼에도 불구하고 `hello`와 같은 정의는 호출될 때마다 동일한 결과를 반환하는 인수가 없는 함수 대신 해당 값을 _직접_ 참조하는 이름을 도입합니다.

### 함수 정의하기

Lean에서는 기능을 정의하는 다양한 방법이 있습니다. 가장 간단한 방법은 정의 타입 앞에 함수의 인수를 공백으로 구분하여 배치하는 것입니다. 예를 들어, 인수에 1을 추가하는 함수는 다음과 같이 작성할 수 있습니다.

```lean
def add1 (n : Nat) : Nat := n + 1
```

`#eval`을 사용하여 이 함수를 테스트하면 예상대로 `8`이 제공됩니다.

```lean
#eval add1 7
```

함수가 각 인수 사이에 공백을 써서 여러 인수에 적용되는 것처럼, 여러 인수를 허용하는 함수는 인수 이름과 타입 사이에 공백을 두고 정의됩니다. 결과가 두 인수 중 가장 큰 것과 동일한 `maximum` 함수는 두 개의 `Nat` 인수 `n` 및 `k`을 취하고 `Nat`을 반환합니다.

```lean
def maximum (n : Nat) (k : Nat) : Nat :=
  if n < k then
    k
  else n
```

마찬가지로 `spaceBetween` 함수는 두 문자열을 사이에 공백을 두고 결합합니다.

```lean
def spaceBetween (before : String) (after : String) : String :=
  String.append before (String.append " " after)
```

`maximum`과 같은 정의된 함수에 인수가 제공되면 먼저 인수 이름을 본문에 제공된 값으로 바꾼 다음 결과 본문을 평가하여 결과가 결정됩니다. 예를 들어:

```lean
maximum (5 + 8) (2 * 7)
===>
maximum 13 14
===>
if 13 < 14 then 14 else 13
===>
14
```

자연수, 정수 및 문자열로 평가되는 표현식에는 다음과 같은 타입이 있습니다(각각 `Nat`, `Int` 및 `String`). 
 이는 함수의 경우에도 마찬가지입니다. 
 `Nat`을 받아들이고 `Bool`을 반환하는 함수의 타입은 `Nat → Bool`이고, 두 개의 `Nat`을 받아들이고 `Nat`을 반환하는 함수의 타입은 `Nat → Nat → Nat`입니다.

특별한 경우로 Lean은 해당 이름이 `#check`과 함께 직접 사용될 때 함수의 서명을 반환합니다. 
 `#check add1`을 입력하면 `add1 (n : Nat) : Nat`이 생성됩니다. 
 그러나 Lean은 함수 이름을 괄호 안에 써서 함수 타입을 표시하도록 "속일" 수 있으며, 이로 인해 함수는 일반 표현식으로 처리되므로 `#check (add1)`은 `add1 : Nat → Nat`을 생성하고 `#check (maximum)`는 `maximum : Nat → Nat → Nat`을 생성합니다. 
 이 화살표는 ASCII 대체 화살표 `->`을 사용하여 작성할 수도 있으므로 이전 함수 타입을 각각 `example : Nat -> Nat := add1` 및 `example : Nat -> Nat -> Nat := maximum`로 작성할 수 있습니다.

배후에서 모든 함수는 실제로 정확히 하나의 인수를 기대합니다. 
 두 개 이상의 인수를 취하는 것처럼 보이는 `maximum`과 같은 함수는 사실 하나의 인수를 취한 다음 새 함수를 반환하는 함수입니다. 
 이 새로운 함수는 다음 인수를 취하고, 더 이상 인수가 필요하지 않을 때까지 프로세스가 계속됩니다. 
 이는 다중 인수 함수에 하나의 인수를 제공하여 볼 수 있습니다. `#check maximum 3`은 `maximum 3 : Nat → Nat`을 생성하고 `#check spaceBetween "Hello "`은 `spaceBetween "Hello " : String → String`을 생성합니다. 
 다중 인수 함수를 구현하기 위해 함수를 반환하는 함수를 사용하는 것을 수학자 Haskell Curry의 이름을 따서 _currying_이라고 합니다. 
 함수 화살표는 오른쪽에 연결됩니다. 즉, `Nat → Nat → Nat`을 괄호 `Nat → (Nat → Nat)`로 묶어야 합니다.

#### 연습문제

* 두 번째와 세 번째 인수 사이에 첫 번째 인수를 배치하여 새 문자열을 생성하는 `String → String → String → String` 타입으로 `joinStringsWith` 함수를 정의합니다. `joinStringsWith ", " "one" "and another"`는 `"one, and another"`으로 평가되어야 합니다. 
 * `joinStringsWith ": "`의 타입은 무엇입니까? Lean으로 답을 확인해보세요. 
 * 주어진 높이, 너비 및 깊이로 직사각형 프리즘의 부피를 계산하는 `Nat → Nat → Nat → Nat` 타입을 사용하여 `volume` 함수를 정의합니다.

#### 타입 정의하기

대부분의 타입 프로그래밍 언어에는 C의 `typedef`과 같이 타입에 대한 별칭을 정의하는 수단이 있습니다. 
 그러나 Lean에서 타입은 언어의 최고 수준의 부분입니다. 다른 타입과 마찬가지로 표현입니다. 
 이는 정의가 다른 값을 참조할 수 있을 뿐만 아니라 타입을 참조할 수 있음을 의미합니다.

예를 들어, `String`이 입력하기에 너무 많은 경우 더 짧은 약어 `Str`을 정의할 수 있습니다.

```lean
def Str : Type := String
```

그러면 `String` 대신 `Str`을 정의 타입으로 사용할 수 있습니다.

```lean
def aStr : Str := "This is a string."
```

이것이 작동하는 이유는 타입이 나머지 Lean과 동일한 규칙을 따르기 때문입니다. 
 타입은 표현식이며, 표현식에서 정의된 이름은 해당 정의로 대체될 수 있습니다. 
 `Str`은 `String`을 의미하도록 정의되었으므로 `aStr`의 정의가 의미가 있습니다.

#### 자주 만나는 메시지

타입에 대한 정의를 사용하여 실험하는 것은 Lean이 오버로드된 정수 리터럴을 지원하는 방식으로 인해 더욱 복잡해졌습니다. 
 `Nat`이 너무 짧으면 더 긴 이름 `NaturalNumber`을 정의할 수 있습니다.

```lean
def NaturalNumber : Type := Nat
```

그러나 `Nat` 대신 `NaturalNumber`을 정의 타입으로 사용하면 예상한 효과가 없습니다. 
 특히 정의는 다음과 같습니다.

```lean
def thirtyEight : NaturalNumber := 38
```

다음 오류가 발생합니다.

```text
failed to synthesize
  OfNat NaturalNumber 38
numerals are polymorphic in Lean, but the numeral `38` cannot be used in a context where the expected type is
  NaturalNumber
due to the absence of the instance above

Hint: Additional diagnostic information may be available using the `set_option diagnostics true` command.
```

이 오류는 Lean이 숫자 리터럴의 _오버로드_를 허용하기 때문에 발생합니다. 
 그렇게 하는 것이 타당한 경우, 마치 해당 타입이 시스템에 내장된 것처럼 새로운 타입에 자연수 리터럴을 사용할 수 있습니다. 
 이는 수학을 편리하게 표현하려는 Lean 사명의 일부이며, 수학의 다양한 분야에서는 매우 다른 목적으로 숫자 표기법을 사용합니다. 
 이 오버로드를 허용하는 특정 기능은 오버로드를 찾기 전에 정의된 모든 이름을 해당 정의로 바꾸지 않으며, 이로 인해 위의 오류 메시지가 발생합니다.

이 제한을 해결하는 한 가지 방법은 정의 오른쪽에 `Nat` 타입을 제공하여 `Nat`의 오버로드 규칙이 `38`에 사용되도록 하는 것입니다.

```lean
def thirtyEight : NaturalNumber := (38 : Nat)
```

`NaturalNumber`은 정의에 따라 `Nat`과 동일한 타입이므로 정의는 여전히 타입이 정확합니다!

또 다른 해결책은 `Nat`에 대한 오버로드와 동일하게 작동하는 `NaturalNumber`에 대한 오버로드를 정의하는 것입니다. 
 그러나 이를 위해서는 Lean의 고급 기능이 필요합니다.

마지막으로 `def` 대신 `abbrev`을 사용하여 `Nat`의 새 이름을 정의하면 정의된 이름을 해당 정의로 바꾸는 오버로드 해결이 가능합니다. 
 `abbrev`을 사용하여 작성된 정의는 항상 펼쳐집니다. 
 예를 들어,

```lean
abbrev N : Type := Nat
```

그리고

```lean
def thirtyNine : N := 39
```

문제없이 받아들여집니다.

내부적으로 일부 정의는 오버로드 해결 중에 펼칠 수 없는 것으로 내부적으로 표시되지만 다른 정의는 그렇지 않습니다. 
 펼쳐질 정의를 _reducible_이라고 합니다. 
 Lean의 확장을 위해서는 축소성에 대한 제어가 필수적입니다. 모든 정의를 완전히 펼치면 기계가 처리하는 속도가 느리고 사용자가 이해하기 어려운 매우 큰 타입이 생성될 수 있습니다. 
 `abbrev`으로 생성된 정의는 축소 가능한 것으로 표시됩니다.

프로그램 작성의 첫 번째 단계는 일반적으로 문제 영역의 개념을 식별한 다음 코드에서 해당 개념에 대한 적절한 표현을 찾는 것입니다. 
 때때로 도메인 개념은 다른 더 간단한 개념의 모음입니다. 
 이 경우 이러한 간단한 구성 요소를 하나의 "패키지"로 그룹화한 다음 의미 있는 이름을 지정하는 것이 편리할 수 있습니다. 
 Lean에서는 이는 C 또는 Rust의 `struct`s 및 C#의 `record`s와 유사한 _structures_를 사용하여 수행됩니다.

구조를 정의하면 다른 타입으로 축소될 수 없는 완전히 새로운 타입이 Lean에 도입됩니다. 
 이는 여러 구조가 동일한 데이터를 포함하더라도 서로 다른 개념을 나타낼 수 있기 때문에 유용합니다. 
 예를 들어, 점은 부동 소수점 숫자 쌍인 데카르트 좌표 또는 극좌표를 사용하여 표현될 수 있습니다. 
 별도의 구조를 정의하면 API 클라이언트가 서로 혼동하는 것을 방지할 수 있습니다.

Lean의 부동 소수점 숫자 타입은 `Float`이라고 하며 부동 소수점 숫자는 일반적인 표기법으로 작성됩니다.

```lean
#check 1.2
```

```text
1.2 : Float
```

```lean
#check -454.2123215
```

```text
-454.2123215 : Float
```

```lean
#check 0.0
```

```text
0.0 : Float
```

부동 소수점 숫자가 소수점으로 쓰여지면 Lean은 `Float` 타입을 추론합니다. 이 항목 없이 작성된 경우 타입 주석이 필요할 수 있습니다.

```lean
#check 0
```

```text
0 : Nat
```

```lean
#check (0 : Float)
```

```text
0 : Float
```

데카르트 점은 `x` 및 `y`라는 두 개의 `Float` 필드가 있는 구조입니다. 
 이는 `structure` 키워드를 사용하여 선언됩니다.

```lean
structure Point where
  x : Float
  y : Float
```

이 선언 이후에는 `Point`이 새로운 구조 타입입니다. 
 구조 타입의 값을 생성하는 일반적인 방법은 중괄호 안에 모든 필드에 값을 제공하는 것입니다. 
 데카르트 평면의 원점은 `x` 및 `y`이 모두 0인 곳입니다.

```lean
def origin : Point := { x := 0.0, y := 0.0 }
```

`#eval origin`의 결과는 `origin`의 정의와 매우 유사합니다.

```text
{ x := 0.000000, y := 0.000000 }
```

구조는 데이터 모음을 "묶어" 이름을 지정하고 단일 단위로 처리하기 위해 존재하므로 구조의 개별 필드를 추출할 수 있는 것도 중요합니다. 
 이는 C, Python, Rust 또는 JavaScript에서와 같이 점 표기법을 사용하여 수행됩니다.

```lean
#eval origin.x
```

```text
0.000000
```

```lean
#eval origin.y
```

```text
0.000000
```

이는 구조를 인수로 사용하는 함수를 정의하는 데 사용할 수 있습니다. 
 예를 들어 점 추가는 기본 좌표 값을 추가하여 수행됩니다. 
 그래야만 한다

```lean
#eval addPoints { x := 1.5, y := 32 } { x := -8, y := 0.2 }
```

수확량

```text
{ x := -6.500000, y := 32.200000 }
```

함수 자체는 `p1` 및 `p2`라는 두 개의 `Point`을 인수로 사용합니다. 
 결과 포인트는 `p1` 및 `p2`의 `x` 및 `y` 필드를 기반으로 합니다.

```lean
def addPoints (p1 : Point) (p2 : Point) : Point :=
  { x := p1.x + p2.x, y := p1.y + p2.y }
```

마찬가지로, `x` 및 `y` 구성 요소의 차이 제곱합의 제곱근인 두 점 사이의 거리는 다음과 같이 쓸 수 있습니다.

```lean
def distance (p1 : Point) (p2 : Point) : Float :=
  Float.sqrt (((p2.x - p1.x) ^ 2.0) + ((p2.y - p1.y) ^ 2.0))
```

예를 들어 $`(1, 2)`과 $`(5, -1)` 사이의 거리는 $`5`입니다.

```lean
#eval distance { x := 1.0, y := 2.0 } { x := 5.0, y := -1.0 }
```

```text
5.000000
```

여러 구조에 동일한 이름을 가진 필드가 있을 수 있습니다. 
 3차원 포인트 데이터 타입은 `x` 및 `y` 필드를 공유할 수 있으며 동일한 필드 이름으로 인스턴스화될 수 있습니다.

```lean
structure Point3D where
  x : Float
  y : Float
  z : Float
```

```lean
def origin3D : Point3D := { x := 0.0, y := 0.0, z := 0.0 }
```

이는 중괄호 구문을 사용하려면 구조의 예상 타입을 알아야 함을 의미합니다. 
 타입을 알 수 없으면 Lean은 구조를 인스턴스화할 수 없습니다. 
 예를 들어,

```lean
#check { x := 0.0, y := 0.0 }
```

오류가 발생합니다

```text
invalid {...} notation, expected type is not known
```

평소와 같이 타입 주석을 제공하여 상황을 해결할 수 있습니다.

```lean
#check ({ x := 0.0, y := 0.0 } : Point)
```

```text
{ x := 0.0, y := 0.0 } : Point
```

프로그램을 더욱 간결하게 만들기 위해 Lean은 중괄호 안에 구조 타입 주석을 허용합니다.

```lean
#check { x := 0.0, y := 0.0 : Point}
```

```text
{ x := 0.0, y := 0.0 } : Point
```

## 구조체 업데이트

`Point`의 `x` 필드를 `0`로 바꾸는 함수 `zeroX`을 상상해 보세요. 
 대부분의 프로그래밍 언어 커뮤니티에서 이 문장은 `x`이 가리키는 메모리 위치를 새로운 값으로 덮어쓰게 된다는 의미입니다. 
 그러나 Lean은 함수형 프로그래밍 언어입니다. 
 함수형 프로그래밍 커뮤니티에서 이러한 종류의 설명이 거의 항상 의미하는 것은 새로운 `Point`이 새 값을 가리키는 `x` 필드와 입력의 원래 값을 가리키는 다른 모든 필드와 함께 할당된다는 것입니다. 
 `zeroX`을 작성하는 한 가지 방법은 이 설명을 문자 그대로 따라 `x`에 대한 새 값을 입력하고 `y`을 수동으로 전송하는 것입니다.

```lean
def zeroX (p : Point) : Point :=
  { x := 0, y := p.y }
```

그러나 이러한 프로그래밍 스타일에는 단점이 있습니다. 
 우선, 새로운 필드가 구조에 추가되면 필드를 업데이트하는 모든 사이트가 업데이트되어야 하므로 유지 관리가 어려워집니다. 
 둘째, 구조에 동일한 타입의 여러 필드가 포함된 경우 복사하여 붙여넣기 코딩으로 인해 필드 내용이 중복되거나 전환될 위험이 있습니다. 
 마지막으로 프로그램은 길고 관료적이 됩니다.

Lean은 구조의 일부 필드를 교체하고 나머지 필드는 그대로 두는 편리한 구문을 제공합니다. 
 이는 구조 초기화에서 `with` 키워드를 사용하여 수행됩니다. 
 변경되지 않은 필드의 소스는 `with` 이전에 발생하고 새 필드는 이후에 발생합니다. 
 예를 들어, `zeroX`는 새로운 `x` 값만 사용하여 작성할 수 있습니다.

```lean
def zeroX (p : Point) : Point :=
  { p with x := 0 }
```

이 구조 업데이트 구문은 기존 값을 수정하지 않으며 일부 필드를 이전 값과 공유하는 새 값을 생성한다는 점을 기억하십시오. 
 `fourAndThree` 지점을 고려하면:

```lean
def fourAndThree : Point :=
  { x := 4.3, y := 3.4 }
```

이를 평가한 다음 `zeroX`을 사용하여 업데이트를 평가한 다음 다시 평가하면 원래 값이 생성됩니다.

```lean
#eval fourAndThree
```

```text
{ x := 4.300000, y := 3.400000 }
```

```lean
#eval zeroX fourAndThree
```

```text
{ x := 0.000000, y := 3.400000 }
```

```lean
#eval fourAndThree
```

```text
{ x := 4.300000, y := 3.400000 }
```

구조 업데이트가 원래 구조를 수정하지 않는다는 사실의 한 가지 결과는 새 값이 이전 값에서 계산되는 경우를 추론하는 것이 더 쉬워진다는 것입니다. 
 이전 구조에 대한 모든 참조는 제공된 모든 새 값에서 동일한 필드 값을 계속 참조합니다.

# 비하인드 스토리

모든 구조에는 _constructor_가 있습니다. 
 여기서 "생성자"라는 용어는 혼란의 원인이 될 수 있습니다. 
 Java 또는 Python과 같은 언어의 생성자와 달리 Lean의 생성자는 데이터 타입이 초기화될 때 실행되는 임의의 코드가 아닙니다. 
 대신 생성자는 새로 할당된 데이터 구조에 저장될 데이터를 수집합니다. 
 데이터를 전처리하거나 유효하지 않은 인수를 거부하는 사용자 정의 생성자를 제공하는 것은 불가능합니다. 
 이것은 실제로 "생성자"라는 단어가 두 가지 맥락에서 서로 다르지만 관련된 의미를 갖는 경우입니다.

기본적으로 `S`이라는 구조의 생성자의 이름은 `S.mk`입니다. 
 여기서 `S`는 네임스페이스 한정자이고 `mk`은 생성자 자체의 이름입니다. 
 중괄호 초기화 구문을 사용하는 대신 생성자를 직접 적용할 수도 있습니다.

```lean
#check Point.mk 1.5 2.8
```

그러나 이는 일반적으로 좋은 Lean 스타일로 간주되지 않으며 Lean은 표준 구조 초기화 구문을 사용하여 피드백을 반환하기도 합니다.

```text
{ x := 1.5, y := 2.8 } : Point
```

생성자에는 함수 타입이 있습니다. 즉, 함수가 필요한 어느 곳에서나 사용할 수 있습니다. 
 예를 들어, `Point.mk`은 두 개의 `Float`(각각 `x` 및 `y`)을 허용하고 새 `Point`을 반환하는 함수입니다.

```lean
#check (Point.mk)
```

```text
Point.mk : Float → Float → Point
```

구조체의 생성자 이름을 재정의하려면 처음에 두 개의 콜론을 사용하여 작성하세요. 
 예를 들어, `Point.mk` 대신 `Point.point`을 사용하려면 다음과 같이 작성하십시오.

```lean
structure Point where
  point ::
  x : Float
  y : Float
```

생성자 외에도 구조체의 각 필드에 대해 접근자 함수가 정의됩니다. 
 이들은 구조의 네임스페이스에 있는 필드와 동일한 이름을 갖습니다. 
 `Point`의 경우 접근자 함수 `Point.x` 및 `Point.y`이 생성됩니다.

```lean
#check (Point.x)
```

```text
Point.x : Point → Float
```

```lean
#check (Point.y)
```

```text
Point.y : Point → Float
```

실제로 중괄호 구조 생성 구문이 뒤에서 구조 생성자에 대한 호출로 변환되는 것처럼 `addPoints`의 이전 정의에 있는 `x` 구문은 `x` 접근자에 대한 호출로 변환됩니다. 
 즉, `#eval origin.x` 및 `#eval Point.x origin` 둘 다 결과가 나옵니다.

```text
0.000000
```

접근자 점 표기법은 구조 필드 이상의 용도로 사용할 수 있습니다. 
 임의 개수의 인수를 취하는 함수에도 사용할 수 있습니다. 
 보다 일반적으로 접근자 표기법은 `TARGET.f ARG1 ARG2 ...` 형식을 갖습니다. 
 `TARGET`의 타입이 `T`인 경우 `T.f`이라는 함수가 호출됩니다. 
 `TARGET`는 `T` 타입의 가장 왼쪽 인수가 됩니다. 이는 항상 첫 번째 인수인 경우가 많지만 `ARG1 ARG2 ...`은 나머지 인수로 순서대로 제공됩니다. 
 예를 들어, `String.append`은 `String`이 `append` 필드가 있는 구조가 아니더라도 접근자 표기법이 있는 문자열에서 호출될 수 있습니다.

```lean
#eval "one string".append " and another"
```

```text
"one string and another"
```

이 예에서 `TARGET`은 `"one string"`을 나타내고 `ARG1`은 `" and another"`을 나타냅니다.

`Point.modifyBoth` 함수(즉, `Point` 네임스페이스에 정의된 `modifyBoth`)는 `Point`의 두 필드 모두에 함수를 적용합니다.

```lean
def Point.modifyBoth (f : Float → Float) (p : Point) : Point :=
  { x := f p.x, y := f p.y }
```

`Point` 인수가 함수 인수 뒤에 오더라도 점 표기법과 함께 사용할 수도 있습니다.

```lean
#eval fourAndThree.modifyBoth Float.floor
```

```text
{ x := 4.000000, y := 3.000000 }
```

이 경우 `TARGET`은 `fourAndThree`을 나타내고 `ARG1`은 `Float.floor`을 나타냅니다. 
 이는 접근자 표기법의 대상이 반드시 첫 번째 인수가 아닌 타입이 일치하는 첫 번째 인수로 사용되기 때문입니다.

### 연습문제

* 직사각형 프리즘의 높이, 너비, 깊이를 각각 `Float`로 포함하는 `RectangularPrism`이라는 구조를 정의합니다. 
 * 직사각형 프리즘의 부피를 계산하는 `volume : RectangularPrism → Float`라는 함수를 정의합니다. 
 * 끝점으로 선분을 나타내는 `Segment`이라는 구조를 정의하고 선분의 길이를 계산하는 함수 `length : Segment → Float`를 정의합니다. `Segment`에는 최대 2개의 필드가 있어야 합니다. 
 * `RectangularPrism` 선언으로 어떤 이름이 소개됩니까? 
 * `Hamster` 및 `Book`의 다음 선언에 의해 도입된 이름은 무엇입니까? 그들의 타입은 무엇입니까?

```lean
    structure Hamster where
      name : String
      fluffy : Bool
    ```

```lean
    structure Book where
      makeBook ::
      title : String
      author : String
      price : Float
    ```

구조를 사용하면 여러 개의 독립적인 데이터 조각을 새로운 타입으로 표현되는 일관된 전체로 결합할 수 있습니다. 
 값 모음을 함께 그룹화하는 구조와 같은 타입을 _제품 타입_이라고 합니다. 
 그러나 많은 도메인 개념은 자연스럽게 구조로 표현될 수 없습니다. 
 예를 들어, 일부 사용자는 문서 소유자이고 일부는 문서를 편집할 수 있으며 다른 사용자는 문서를 읽기만 할 수 있는 경우 응용 프로그램은 사용자 권한을 추적해야 할 수 있습니다. 
 계산기에는 덧셈, 뺄셈, 곱셈과 같은 다양한 이진 연산자가 있습니다. 
 구조는 다중 선택 항목을 인코딩하는 쉬운 방법을 제공하지 않습니다.

마찬가지로, 구조는 고정된 필드 집합을 추적하는 훌륭한 방법이지만 많은 응용 프로그램에는 임의의 수의 요소를 포함할 수 있는 데이터가 필요합니다. 
 트리 및 목록과 같은 대부분의 고전적인 데이터 구조는 목록의 꼬리 자체가 목록이거나 이진 트리의 왼쪽 및 오른쪽 분기 자체가 이진 트리인 재귀 구조를 갖습니다. 
 앞서 언급한 계산기에서는 표현식 자체의 구조가 재귀적입니다. 
 예를 들어 덧셈 표현식의 합은 그 자체로 곱셈 표현식일 수 있습니다.

선택을 허용하는 데이터 타입을 _합계 타입_이라고 하며 자신의 인스턴스를 포함할 수 있는 데이터 타입을 _재귀 데이터 타입_이라고 합니다. 
 재귀적 합계 타입을 _귀납적 데이터 타입_이라고 합니다. 왜냐하면 수학적 귀납법을 사용하여 이에 대한 진술을 증명할 수 있기 때문입니다. 
 프로그래밍할 때 귀납적 데이터 타입은 패턴 일치 및 재귀 함수를 통해 소비됩니다.

내장 타입 중 상당수는 실제로 표준 라이브러리의 귀납적 데이터 타입입니다. 
 예를 들어 `Bool`은 귀납적 데이터 타입입니다.

```lean
inductive Bool where
  | false : Bool
  | true : Bool
```

이 정의는 두 가지 주요 부분으로 구성됩니다. 
 첫 번째 줄은 새 타입의 이름(`Bool`)을 제공하고 나머지 줄은 각각 생성자를 설명합니다. 
 구조 생성자와 마찬가지로 귀납적 데이터 타입의 생성자는 임의의 초기화 및 검증 코드를 삽입하는 장소가 아니라 다른 데이터의 단순한 비활성 수신자이자 컨테이너입니다. 
 구조와 달리 귀납적 데이터 타입에는 여러 생성자가 있을 수 있습니다. 
 여기에는 `true` 및 `false`라는 두 개의 생성자가 있으며 둘 다 인수를 사용하지 않습니다. 
 구조 선언이 선언된 타입의 이름을 딴 네임스페이스에 이름을 배치하는 것처럼 귀납적 데이터 타입은 생성자의 이름을 네임스페이스에 배치합니다. 
 Lean 표준 라이브러리에서 `true` 및 `false`는 각각 `Bool.true` 및 `Bool.false`이 아닌 단독으로 작성할 수 있도록 이 네임스페이스에서 다시 내보내집니다.

데이터 모델링 관점에서 볼 때 귀납적 데이터 타입은 봉인된 추상 클래스가 다른 언어에서 사용될 수 있는 것과 동일한 많은 컨텍스트에서 사용됩니다. 
 C# 또는 Java와 같은 언어에서는 `Bool`에 대한 유사한 정의를 작성할 수 있습니다.```
abstract class Bool {}
class True : Bool {}
class False : Bool {}
```그러나 이러한 표현의 세부 사항은 상당히 다릅니다. 특히 각각의 비추상 클래스는 데이터를 할당하는 새로운 타입과 새로운 방법을 모두 생성합니다. 객체 지향 예에서 `True` 및 `False`은 둘 다 `Bool`보다 더 구체적인 타입인 반면 Lean 정의에서는 새로운 타입 `Bool`만 도입합니다.

음수가 아닌 정수의 타입 `Nat`은 귀납적 데이터 타입입니다.

```lean
inductive Nat where
  | zero : Nat
  | succ (n : Nat) : Nat
```

여기서 `zero`은 0을 나타내고 `succ`은 다른 숫자의 후속 숫자를 나타냅니다. 
 `succ`의 선언에 언급된 `Nat`는 정의 중인 바로 그 타입 `Nat`입니다. 
 _Successor_는 "보다 큰 1"을 의미하므로 5의 후속자는 6이고 32,185의 후속자는 32,186입니다. 
 이 정의를 사용하면 `4`는 `Nat.succ (Nat.succ (Nat.succ (Nat.succ Nat.zero)))`으로 표시됩니다. 
 이 정의는 이름이 약간 다른 `Bool`의 정의와 거의 유사합니다. 
 유일한 실제 차이점은 `succ` 뒤에 `(n : Nat)`이 따라온다는 것입니다. 이는 생성자 `succ`이 `n`라는 이름의 `Nat` 타입 인수를 취함을 지정합니다. 
 `zero` 및 `succ` 이름은 해당 타입에 따라 명명된 네임스페이스에 있으므로 각각 `Nat.zero` 및 `Nat.succ`으로 참조해야 합니다.

`n`과 같은 인수 이름은 Lean의 오류 메시지와 수학적 증명을 작성할 때 제공되는 피드백에 나타날 수 있습니다. 
 Lean에는 이름으로 인수를 제공하기 위한 선택적 구문도 있습니다. 
 그러나 일반적으로 인수 이름 선택은 API의 큰 부분을 구성하지 않기 때문에 구조 필드 이름 선택보다 덜 중요합니다.

C# 또는 Java에서는 `Nat`을 다음과 같이 정의할 수 있습니다.```
abstract class Nat {}
class Zero : Nat {}
class Succ : Nat {
    public Nat n;
    public Succ(Nat pred) {
        n = pred;
    }
}
```위의 `Bool` 예와 마찬가지로 이는 Lean에 상응하는 것보다 더 많은 타입을 정의합니다. 
 또한 이 예에서는 Lean 데이터 타입 생성자가 C# 또는 Java의 생성자보다 추상 클래스의 하위 클래스와 훨씬 더 유사한 점을 강조합니다. 여기에 표시된 생성자에는 실행될 초기화 코드가 포함되어 있기 때문입니다.

합계 타입은 문자열 태그를 사용하여 TypeScript에서 식별된 공용체를 인코딩하는 것과 유사합니다. 
 TypeScript에서 `Nat`은 다음과 같이 정의될 수 있습니다.```
interface Zero {
    tag: "zero";
}

interface Succ {
    tag: "succ";
    predecessor: Nat;
}

type Nat = Zero | Succ;
```C# 및 Java와 마찬가지로 이 인코딩은 Lean보다 더 많은 타입으로 끝납니다. `Zero` 및 `Succ`은 각각 자체 타입이기 때문입니다. 
 이는 또한 Lean 생성자가 내용을 식별하는 태그를 포함하는 JavaScript 또는 TypeScript의 객체에 해당한다는 것을 보여줍니다.

# 패턴 매칭

많은 언어에서 이러한 종류의 데이터는 먼저 인스턴스 연산자를 사용하여 어떤 하위 클래스가 수신되었는지 확인한 다음 해당 하위 클래스에서 사용할 수 있는 필드의 값을 읽어 소비됩니다. 
 검사 인스턴스는 실행할 코드를 결정하여 이 코드에 필요한 데이터를 사용할 수 있는지 확인하고 필드 자체는 데이터를 제공합니다. 
 Lean에서는 이 두 가지 목적이 모두 _패턴 일치_에 의해 동시에 제공됩니다.

패턴 일치를 사용하는 함수의 예로는 `isZero`이 있습니다. 이 함수는 인수가 `Nat.zero`일 때 `true`을 반환하고, 그렇지 않으면 false를 반환합니다.

```lean
def isZero (n : Nat) : Bool :=
  match n with
  | Nat.zero => true
  | Nat.succ k => false
```

`match` 표현식에는 구조 분해를 위한 함수의 인수 `n`이 제공됩니다. 
 `Nat.zero`에 의해 `n`이 생성된 경우 패턴 일치의 첫 번째 분기가 선택되고 결과는 `true`입니다. 
 `Nat.succ`에 의해 `n`이 생성된 경우 두 번째 분기가 선택되고 결과는 `false`입니다.

`isZero Nat.zero`의 평가는 단계별로 다음과 같이 진행됩니다.

```lean
isZero Nat.zero
===>
match Nat.zero with
| Nat.zero => true
| Nat.succ k => false
===>
true
```

`isZero 5` 평가는 비슷하게 진행됩니다.

```lean
isZero 5
===>
isZero (Nat.succ (Nat.succ (Nat.succ (Nat.succ (Nat.succ Nat.zero)))))
===>
match Nat.succ (Nat.succ (Nat.succ (Nat.succ (Nat.succ Nat.zero)))) with
| Nat.zero => true
| Nat.succ k => false
===>
false
```

`isZero`에 있는 패턴의 두 번째 분기에 있는 `k`은 장식용이 아닙니다. 
 제공된 이름으로 `Nat.succ`에 대한 인수인 `Nat`을 표시합니다. 
 그러면 더 작은 숫자를 사용하여 표현식의 최종 결과를 계산할 수 있습니다.

어떤 숫자 $`n`의 후속 숫자가 $`n`보다 하나 큰 것처럼(즉, $`n + 1`) 숫자의 선행 숫자는 그 숫자보다 1 작습니다. 
 `pred`이 `Nat`의 선행자를 찾는 함수인 경우 다음 예가 예상된 결과를 찾는 경우여야 합니다.

```lean
#eval pred 5
```

```text
4
```

```lean
#eval pred 839
```

```text
838
```

`Nat`은 음수를 나타낼 수 없기 때문에 `Nat.zero`은 약간의 수수께끼입니다. 
 일반적으로 `Nat`로 작업할 때 일반적으로 음수를 생성하는 연산자는 `zero` 자체를 생성하도록 재정의됩니다.

```lean
#eval pred 0
```
```text
0
```

`Nat`의 이전 항목을 찾으려면 첫 번째 단계는 이를 생성하는 데 사용된 생성자를 확인하는 것입니다. 
 `Nat.zero`인 경우 결과는 `Nat.zero`입니다. 
 `Nat.succ`인 경우 `k`라는 이름은 그 아래의 `Nat`을 참조하는 데 사용됩니다. 
 그리고 이 `Nat`은 원하는 전임자이므로 `Nat.succ` 분기의 결과는 `k`입니다.

```lean
def pred (n : Nat) : Nat :=
  match n with
  | Nat.zero => Nat.zero
  | Nat.succ k => k
```

이 함수를 `5`에 적용하면 다음 단계가 생성됩니다.

```lean
pred 5
===>
pred (Nat.succ 4)
===>
match Nat.succ 4 with
| Nat.zero => Nat.zero
| Nat.succ k => k
===>
4
```

패턴 일치는 구조 및 합계 타입과 함께 사용할 수 있습니다. 
 예를 들어 `Point3D`에서 3차원을 추출하는 함수는 다음과 같이 작성할 수 있습니다.

```lean
def depth (p : Point3D) : Float :=
  match p with
  | { x:= h, y := w, z := d } => d
```

이 경우에는 `Point3D.z` 접근자를 사용하는 것이 훨씬 더 간단했지만 구조 패턴은 때때로 함수를 작성하는 가장 간단한 방법입니다.

### 재귀 함수

정의되는 이름을 참조하는 정의를 _재귀적 정의_라고 합니다. 
 귀납적 데이터 타입은 재귀적일 수 있습니다. 실제로 `Nat`은 `succ`이 또 다른 `Nat`을 요구하기 때문에 그러한 데이터 타입의 예입니다. 
 재귀 데이터 타입은 사용 가능한 메모리와 같은 기술적 요인에 의해서만 제한되는 임의의 대규모 데이터를 나타낼 수 있습니다. 
 데이터 타입 정의의 각 자연수에 대해 하나의 생성자를 기록하는 것이 불가능한 것처럼 각 가능성에 대한 패턴 일치 사례를 기록하는 것도 불가능합니다.

재귀 데이터 타입은 재귀 함수로 훌륭하게 보완됩니다. 
 `Nat`에 대한 간단한 재귀 함수는 인수가 짝수인지 확인합니다. 
 이 경우 `Nat.zero`은 짝수입니다. 
 이와 같은 코드의 비재귀 분기를 _기본 사례_라고 합니다. 
 홀수의 계승자는 짝수, 짝수의 계승자는 홀수이다. 
 이는 `Nat.succ`로 작성된 숫자가 인수가 짝수가 아닌 경우에만 짝수임을 의미합니다.

```lean
def even (n : Nat) : Bool :=
  match n with
  | Nat.zero => true
  | Nat.succ k => not (even k)
```

이러한 사고 패턴은 `Nat`에 재귀 함수를 작성할 때 일반적입니다. 
 먼저 `Nat.zero`에 대해 무엇을 해야 할지 파악하세요. 
 그런 다음 임의의 `Nat`에 대한 결과를 후속 결과에 대한 결과로 변환하는 방법을 결정하고 이 변환을 재귀 호출의 결과에 적용합니다. 
 이 패턴을 _구조적 재귀_라고 합니다.

많은 언어와 달리 Lean은 기본적으로 모든 재귀 함수가 결국 기본 사례에 도달하도록 보장합니다. 
 프로그래밍 관점에서 이는 우발적인 무한 루프를 배제합니다. 
 그러나 이 기능은 무한 루프가 큰 어려움을 야기하는 정리를 증명할 때 특히 중요합니다. 
 결과적으로 Lean은 원래 번호에서 자신을 재귀적으로 호출하려고 시도하는 `even` 버전을 허용하지 않습니다.

```lean
def evenLoops (n : Nat) : Bool :=
  match n with
  | Nat.zero => true
  | Nat.succ k => not (evenLoops n)
```오류 메시지의 중요한 부분은 Lean이 재귀 함수가 항상 기본 사례에 도달하는지 확인할 수 없다는 것입니다(그렇지 않기 때문입니다).

```text
fail to show termination for
  evenLoops
with errors
failed to infer structural recursion:
Not considering parameter n of evenLoops:
  it is unchanged in the recursive calls
no parameters suitable for structural recursion

well-founded recursion cannot be used, `evenLoops` does not take any (non-fixed) arguments
```

덧셈이 두 개의 인수를 취하더라도 그 중 하나만 검사하면 됩니다. 
 숫자 $`n`에 0을 추가하려면 $`n`을 반환하면 됩니다. 
 $`k`의 후속 항목을 $`n`에 추가하려면 $`k`을 $`n`에 추가한 결과의 후속 항목을 가져옵니다.

```lean
def plus (n : Nat) (k : Nat) : Nat :=
  match k with
  | Nat.zero => n
  | Nat.succ k' => Nat.succ (plus n k')
```

`plus`의 정의에서 이름 `k'`은 인수 `k`에 연결되지만 동일하지는 않음을 나타내기 위해 선택됩니다. 
 예를 들어 `plus 3 2` 평가를 진행하면 다음 단계가 수행됩니다.

```lean
plus 3 2
===>
plus 3 (Nat.succ (Nat.succ Nat.zero))
===>
match Nat.succ (Nat.succ Nat.zero) with
| Nat.zero => 3
| Nat.succ k' => Nat.succ (plus 3 k')
===>
Nat.succ (plus 3 (Nat.succ Nat.zero))
===>
Nat.succ (match Nat.succ Nat.zero with
| Nat.zero => 3
| Nat.succ k' => Nat.succ (plus 3 k'))
===>
Nat.succ (Nat.succ (plus 3 Nat.zero))
===>
Nat.succ (Nat.succ (match Nat.zero with
| Nat.zero => 3
| Nat.succ k' => Nat.succ (plus 3 k')))
===>
Nat.succ (Nat.succ 3)
===>
5
```

덧셈에 대해 생각하는 한 가지 방법은 $`n + k`이 $`n`에 `Nat.succ` $`k` 번을 적용한다는 것입니다. 
 마찬가지로 $`n × k` 곱셈은 $`n`을 $`k`번 더하고, $`n - k`을 빼면 $`n`의 이전 값인 $`k`번을 취합니다.

```lean
def times (n : Nat) (k : Nat) : Nat :=
  match k with
  | Nat.zero => Nat.zero
  | Nat.succ k' => plus n (times n k')
```

```lean
def minus (n : Nat) (k : Nat) : Nat :=
  match k with
  | Nat.zero => n
  | Nat.succ k' => pred (minus n k')
```

구조적 재귀를 사용하여 모든 함수를 쉽게 작성할 수 있는 것은 아닙니다. 
 반복되는 덧셈 `Nat.succ`, 반복되는 덧셈으로서의 곱셈, 반복되는 전임자로서의 뺄셈을 이해하는 것은 나눗셈을 반복된 뺄셈으로 구현하는 것을 의미합니다. 
 이 경우 분자가 제수보다 작으면 결과는 0입니다. 
 그렇지 않으면 결과는 분자에서 제수를 뺀 값을 제수로 나눈 결과입니다.

```lean
def div (n : Nat) (k : Nat) : Nat :=
  if n < k then
    0
  else Nat.succ (div (n - k) k)
```

두 번째 인수가 `0`이 아닌 한 이 프로그램은 항상 기본 사례를 향해 진행하므로 종료됩니다. 
 그러나 0에 대한 결과를 찾고 더 작은 `Nat`에 대한 결과를 후속 결과에 대한 결과로 변환하는 패턴을 따르지 않기 때문에 구조적으로 재귀적이지 않습니다. 
 특히 함수의 재귀 호출은 입력 생성자의 인수가 아닌 다른 함수 호출의 결과에 적용됩니다. 
 따라서 Lean은 다음 메시지로 이를 거부합니다.

```text
fail to show termination for
  div
with errors
failed to infer structural recursion:
Not considering parameter k of div:
  it is unchanged in the recursive calls
Cannot use parameter k:
  failed to eliminate recursive application
    div (n - k) k

failed to prove termination, possible solutions:
  - Use `have`-expressions to prove the remaining goals
  - Use `termination_by` to specify a different well-founded relation
  - Use `decreasing_by` to specify your own tactic for discharging this kind of goal
k n : Nat
h✝ : ¬n < k
⊢ n - k < n
```

이 메시지는 `div`에 수동 종료 증명이 필요함을 의미합니다. 
 이 주제는 마지막 장에서 탐구됩니다.

대부분의 언어와 마찬가지로 Lean의 타입도 인수를 취할 수 있습니다. 
 예를 들어, `List Nat` 타입은 자연수 목록을 설명하고, `List String` 타입은 문자열 목록을 설명하며, `List (List Point)` 타입은 점 목록을 설명합니다. 
 이는 C# 또는 Java와 같은 언어의 `List<Nat>`, `List<String>` 또는 `List<List<Point>>`와 매우 유사합니다. 
 Lean이 함수에 인수를 전달하기 위해 공백을 사용하는 것처럼, 타입에 인수를 전달하기 위해 공백을 사용합니다.

함수형 프로그래밍에서 _다형성_이라는 용어는 일반적으로 타입을 인수로 사용하는 데이터 타입 및 정의를 나타냅니다. 
 이는 일반적으로 슈퍼클래스의 일부 동작을 재정의할 수 있는 하위 클래스를 지칭하는 객체 지향 프로그래밍 커뮤니티와는 다릅니다. 
 이 책에서 "다형성"은 항상 단어의 첫 번째 의미를 나타냅니다. 
 이러한 타입 인수는 데이터 타입 또는 정의에 사용될 수 있으며, 이를 통해 인수 이름을 다른 타입으로 대체한 결과로 생성된 모든 타입에 동일한 데이터 타입 또는 정의를 사용할 수 있습니다.

`Point` 구조에서는 `x` 및 `y` 필드가 모두 `Float`이어야 합니다. 
 그러나 각 좌표에 대해 특정 표현이 필요한 점은 없습니다. 
 `PPoint`라고 하는 `Point`의 다형성 버전은 타입을 인수로 사용하고 두 필드 모두에 해당 타입을 사용할 수 있습니다.

```lean
structure PPoint (α : Type) where
  x : α
  y : α
```

함수 정의의 인수가 정의되는 이름 바로 뒤에 작성되는 것처럼, 구조체의 인수는 구조체 이름 바로 뒤에 작성됩니다. 
 더 이상 구체적인 이름이 제시되지 않는 경우 Lean에서 타입 인수의 이름을 지정하기 위해 그리스 문자를 사용하는 것이 일반적입니다. 
 `Type`은 다른 타입을 설명하는 타입이므로 `Nat`, `List String` 및 `PPoint Int`은 모두 `Type` 타입을 갖습니다.

`List`과 마찬가지로 `PPoint`은 특정 타입을 인수로 제공하여 사용할 수 있습니다.

```lean
def natOrigin : PPoint Nat :=
  { x := Nat.zero, y := Nat.zero }
```

이 예에서는 두 필드 모두 `Nat`s가 될 것으로 예상됩니다. 
 함수가 인수 변수를 인수 값으로 대체하여 호출되는 것과 마찬가지로 `PPoint`에 `Nat` 타입을 인수로 제공하면 `x` 및 `y` 필드에 `Nat` 타입이 있는 구조가 생성됩니다. 이는 인수 이름 `α`이 인수 타입 `Nat`로 대체되었기 때문입니다. 
 타입은 Lean의 일반 표현식이므로 다형성 타입(예: `PPoint`)에 인수를 전달하는 데 특별한 구문이 필요하지 않습니다.

정의는 타입을 인수로 취하여 다형성을 만들 수도 있습니다. 
 `replaceX` 함수는 `PPoint`의 `x` 필드를 새 값으로 대체합니다. 
 `replaceX`이 _모든_ 다형성 점과 함께 작동하려면 그 자체가 다형성이어야 합니다. 
 이는 첫 번째 인수가 포인트 필드의 타입이 되도록 하고 이후 인수는 첫 번째 인수의 이름을 다시 참조함으로써 달성됩니다.

```lean
def replaceX (α : Type) (point : PPoint α) (newX : α) : PPoint α :=
  { point with x := newX }
```

즉, `point` 및 `newX` 인수의 타입이 `α`을 언급하는 경우 _첫 번째 인수로 제공된 타입_을 참조하는 것입니다. 
 이는 함수 인수 이름이 함수 본문에 나타날 때 제공된 값을 참조하는 방식과 유사합니다.

이는 Lean에게 `replaceX` 타입을 확인하도록 요청한 다음 `replaceX Nat` 타입을 확인하도록 요청하여 확인할 수 있습니다.

```lean
#check (replaceX)
```

```text
replaceX : (α : Type) → PPoint α → α → PPoint α
```

이 함수 타입에는 첫 번째 인수의 _name_이 포함되며, 타입의 이후 인수는 이 이름을 다시 참조합니다. 
 함수 본문에서 인수 이름을 제공된 인수 값으로 대체하여 함수 응용 프로그램의 값을 찾는 것처럼 함수 응용 프로그램의 타입은 함수의 반환 타입에서 인수 이름을 제공된 값으로 대체하여 찾습니다. 
 첫 번째 인수 `Nat`을 제공하면 타입의 나머지 부분에서 `α`이 모두 `Nat`로 대체됩니다.

```lean
#check replaceX Nat
```

```text
replaceX Nat : PPoint Nat → Nat → PPoint Nat
```

나머지 인수는 명시적으로 이름이 지정되지 않았으므로 더 많은 인수가 제공되어도 추가 대체가 발생하지 않습니다.

```lean
#check replaceX Nat natOrigin
```

```text
replaceX Nat natOrigin : Nat → PPoint Nat
```

```lean
#check replaceX Nat natOrigin 5
```

```text
replaceX Nat natOrigin 5 : PPoint Nat
```

전체 함수 적용 표현식의 타입이 타입을 인수로 전달하여 결정되었다는 사실은 이를 평가하는 능력과 관련이 없습니다.

```lean
#eval replaceX Nat natOrigin 5
```

```text
{ x := 5, y := 0 }
```

다형성 함수는 명명된 타입 인수를 사용하고 이후 타입이 인수 이름을 참조하도록 하여 작동합니다. 
 그러나 이름을 지정할 수 있는 타입 인수에는 특별한 것이 없습니다. 
 양수 또는 음수 부호를 나타내는 데이터 타입이 있는 경우:

```lean
inductive Sign where
  | pos
  | neg
```

인수가 부호인 함수를 작성하는 것이 가능합니다. 
 인수가 양수이면 함수는 `Nat`을 반환하고, 음수이면 `Int`을 반환합니다.

```lean
def posOrNegThree (s : Sign) :
    match s with | Sign.pos => Nat | Sign.neg => Int :=
  match s with
  | Sign.pos => (3 : Nat)
  | Sign.neg => (-3 : Int)
```

타입은 일급이고 Lean 언어의 일반 규칙을 사용하여 계산할 수 있으므로 데이터 타입에 대한 패턴 일치를 통해 계산할 수 있습니다. 
 Lean은 이 함수를 검사할 때 함수 본문의 `match` 표현식이 타입의 `match` 표현식에 해당한다는 사실을 사용하여 `Nat`를 `pos` 사례에 대해 예상되는 타입으로 만들고 `Int`를 `neg` 사례에 대해 예상되는 타입으로 만듭니다.

`posOrNegThree`을 `pos`에 적용하면 함수 본문과 해당 반환 타입 모두에서 인수 이름 `s`이 `pos`으로 대체됩니다. 
 평가는 표현식과 해당 타입 모두에서 발생할 수 있습니다.

```lean
(posOrNegThree Sign.pos :
 match Sign.pos with | Sign.pos => Nat | Sign.neg => Int)
===>
((match Sign.pos with
  | Sign.pos => (3 : Nat)
  | Sign.neg => (-3 : Int)) :
 match Sign.pos with | Sign.pos => Nat | Sign.neg => Int)
===>
((3 : Nat) : Nat)
===>
3
```

# 연결리스트

Lean의 표준 라이브러리에는 `List`이라는 정식 연결 목록 데이터 타입과 사용을 더욱 편리하게 해주는 특수 구문이 포함되어 있습니다. 
 목록은 대괄호 안에 작성됩니다. 
 예를 들어, 10보다 작은 소수를 포함하는 목록은 다음과 같이 작성할 수 있습니다.

```lean
def primesUnder10 : List Nat := [2, 3, 5, 7]
```

이면에서 `List`은 다음과 같이 정의된 귀납적 데이터 타입입니다.

```lean
inductive List (α : Type) where
  | nil : List α
  | cons : α → List α → List α
```

표준 라이브러리의 실제 정의는 아직 제시되지 않은 기능을 사용하기 때문에 약간 다르지만 실질적으로 유사합니다. 
 이 정의에 따르면 `List`은 `PPoint`과 마찬가지로 단일 타입을 인수로 사용합니다. 
 이 타입은 목록에 저장된 항목의 타입입니다. 
 생성자에 따르면 `List α`은 `nil` 또는 `cons`를 사용하여 빌드할 수 있습니다. 
 생성자 `nil`은 빈 목록을 나타내고 생성자 `cons`은 비어 있지 않은 목록에 사용됩니다. 
 `cons`의 첫 번째 인수는 목록의 선두이고 두 번째 인수는 목록의 꼬리입니다. 
 $`n` 항목을 포함하는 목록에는 $`n` `cons` 생성자가 포함되어 있으며 마지막 생성자는 `nil`이 꼬리입니다.

`primesUnder10` 예제는 `List`의 생성자를 직접 사용하여 보다 명시적으로 작성할 수 있습니다.

```lean
def explicitPrimesUnder10 : List Nat :=
  List.cons 2 (List.cons 3 (List.cons 5 (List.cons 7 List.nil)))
```

이 두 정의는 완전히 동일하지만 `primesUnder10`은 `explicitPrimesUnder10`보다 읽기가 훨씬 쉽습니다.

`List`을 사용하는 함수는 `Nat`을 사용하는 함수와 거의 동일한 방식으로 정의할 수 있습니다. 
 실제로 연결된 목록을 생각하는 한 가지 방법은 각 `succ` 생성자에 추가 데이터 필드가 매달려 있는 `Nat`로 생각하는 것입니다. 
 이러한 관점에서 목록의 길이를 계산하는 것은 각 `cons`을 `succ`로 바꾸고 마지막 `nil`을 `zero`로 바꾸는 프로세스입니다. 
 `replaceX`이 포인트의 필드 타입을 인수로 취한 것처럼 `length`은 목록 항목의 타입을 취합니다. 
 예를 들어 목록에 문자열이 포함되어 있으면 첫 번째 인수는 `String`: `length String ["Sourdough", "bread"]`입니다. 
 다음과 같이 계산되어야 합니다:

```lean
length String ["Sourdough", "bread"]
===>
length String (List.cons "Sourdough" (List.cons "bread" List.nil))
===>
Nat.succ (length String (List.cons "bread" List.nil))
===>
Nat.succ (Nat.succ (length String List.nil))
===>
Nat.succ (Nat.succ Nat.zero)
===>
2
```

`length`의 정의는 다형성(목록 항목 타입을 인수로 사용하기 때문에)이면서 재귀적(자기 자신을 참조하기 때문에)입니다. 
 일반적으로 함수는 데이터의 모양을 따릅니다. 재귀 데이터 타입은 재귀 함수로 이어지고 다형성 데이터 타입은 다형성 함수로 이어집니다.

```lean
def length (α : Type) (xs : List α) : Nat :=
  match xs with
  | List.nil => Nat.zero
  | List.cons y ys => Nat.succ (length α ys)
```

`xs` 및 `ys`과 같은 이름은 일반적으로 알 수 없는 값 목록을 나타내는 데 사용됩니다. 
 이름의 `s`은 복수형임을 나타내므로 "x s" 및 "y s" 대신 "exes" 및 "whys"로 발음됩니다.

목록의 함수를 더 쉽게 읽을 수 있도록 대괄호 표기법 `[]`을 사용하여 `nil`에 대한 패턴 일치를 수행하고 중위 `::`를 `cons` 대신 사용할 수 있습니다.

```lean
def length (α : Type) (xs : List α) : Nat :=
  match xs with
  | [] => 0
  | y :: ys => Nat.succ (length α ys)
```

# 암시적 인수

`replaceX` 및 `length`은 모두 사용하기에 다소 관료적입니다. 왜냐하면 타입 인수는 일반적으로 나중 값에 의해 고유하게 결정되기 때문입니다. 
 실제로 대부분의 언어에서 컴파일러는 자체적으로 타입 인수를 완벽하게 결정할 수 있으며 가끔씩 사용자의 도움이 필요할 뿐입니다. 
 이는 Lean에서도 마찬가지입니다. 
 함수를 정의할 때 인수를 괄호 대신 중괄호로 묶어 _암시적_으로 선언할 수 있습니다. 
 예를 들어 암시적 타입 인수가 있는 `replaceX` 버전은 다음과 같습니다.

```lean
def replaceX {α : Type} (point : PPoint α) (newX : α) : PPoint α :=
  { point with x := newX }
```

Lean은 이후 인수에서 `α`의 값을 _infer_할 수 있기 때문에 `Nat`을 명시적으로 제공하지 않고도 `natOrigin`과 함께 사용할 수 있습니다.

```lean
#eval replaceX natOrigin 5
```

```text
{ x := 5, y := 0 }
```

마찬가지로 `length`을 재정의하여 항목 타입을 암시적으로 사용할 수 있습니다.

```lean
def length {α : Type} (xs : List α) : Nat :=
  match xs with
  | [] => 0
  | y :: ys => Nat.succ (length ys)
```

이 `length` 함수는 `primesUnder10`에 직접 적용할 수 있습니다.

```lean
#eval length primesUnder10
```

```text
4
```

표준 라이브러리에서 Lean은 이 함수를 `List.length`이라고 부릅니다. 이는 구조 필드 액세스에 사용되는 도트 구문을 사용하여 목록의 길이를 찾을 수도 있음을 의미합니다.

```lean
#eval primesUnder10.length
```

```text
4
```

C#과 Java에서 때때로 형식 인수를 명시적으로 제공해야 하는 것처럼 Lean이 항상 암시적 인수를 찾을 수 있는 것은 아닙니다. 
 이 경우 이름을 사용하여 제공할 수 있습니다. 
 예를 들어 정수 목록에만 작동하는 `List.length` 버전은 `α`을 `Int`로 설정하여 지정할 수 있습니다.

```lean
#check List.length (α := Int)
```

```text
List.length : List Int → Nat
```

# 더 많은 내장 데이터 타입

목록 외에도 Lean의 표준 라이브러리에는 다양한 상황에서 사용할 수 있는 수많은 다른 구조와 귀납적 데이터 타입이 포함되어 있습니다.

## `Option` 
 모든 목록에 첫 번째 항목이 있는 것은 아닙니다. 일부 목록은 비어 있습니다. 
 컬렉션에 대한 많은 작업이 원하는 것을 찾지 못할 수 있습니다. 
 예를 들어, 목록에서 첫 번째 항목을 찾는 함수는 그러한 항목을 찾지 못할 수도 있습니다. 
 따라서 첫 번째 항목이 없음을 알리는 방법이 있어야 합니다.

많은 언어에는 값이 없음을 나타내는 `null` 값이 있습니다. 
 기존 타입에 특별한 `null` 값을 제공하는 대신 Lean은 다른 타입에 누락된 값에 대한 표시기를 제공하는 `Option`라는 데이터 타입을 제공합니다. 
 예를 들어, null을 허용하는 `Int`은 `Option Int`로 표시되고, null을 허용하는 문자열 목록은 `Option (List String)` 타입으로 표시됩니다. 
 null 허용 여부를 나타내는 새로운 타입을 도입한다는 것은 `Int`이 예상되는 컨텍스트에서 `Option Int`을 사용할 수 없기 때문에 타입 시스템이 `null`에 대한 검사를 잊을 수 없음을 보장한다는 것을 의미합니다.

`Option`에는 기본 타입의 null이 아닌 버전과 null 버전을 각각 나타내는 `some` 및 `none`라는 두 개의 생성자가 있습니다. 
 null이 아닌 생성자 `some`에는 기본 값이 포함되어 있지만 `none`에는 인수가 없습니다.

```lean
inductive Option (α : Type) : Type where
  | none : Option α
  | some (val : α) : Option α
```

`Option` 타입은 C# 및 Kotlin과 같은 언어의 null 허용 타입과 매우 유사하지만 동일하지는 않습니다. 
 이러한 언어에서 타입(예: `Boolean`)이 항상 타입(`true` 및 `false`)의 실제 값을 참조하는 경우 `Boolean?` 또는 `Nullable<Boolean>` 타입은 `null` 값을 추가로 허용합니다. 
 타입 시스템에서 이를 추적하는 것은 매우 유용합니다. 타입 검사기와 기타 도구는 프로그래머가 `null`을 확인하는 것을 기억하는 데 도움이 될 수 있으며 타입 서명을 통해 null 허용 여부를 명시적으로 설명하는 API는 그렇지 않은 API보다 더 많은 정보를 제공합니다. 
 그러나 이러한 nullable 타입은 매우 중요한 한 가지 측면에서 Lean의 `Option`과 다릅니다. 즉, 여러 계층의 선택성을 허용하지 않는다는 것입니다. 
 `Option (Option Int)`은 `none`, `some none` 또는 `some (some 360)`로 구성될 수 있습니다. 
 반면에 Kotlin은 `T??`을 `T?`과 동일하게 취급합니다. 
 이 미묘한 차이는 실제로는 거의 관련이 없지만 때때로 중요할 수 있습니다.

목록의 첫 번째 항목을 찾으려면(있는 경우) `List.head?`을 사용하세요. 
 물음표는 이름의 일부이며 C# 또는 Kotlin에서 null 허용 타입을 나타내기 위해 물음표를 사용하는 것과 관련이 없습니다. 
 `List.head?` 정의에서 밑줄은 목록의 끝 부분을 나타내는 데 사용됩니다. 
 패턴에서 밑줄은 무엇이든 일치하지만 일치하는 데이터를 참조하는 변수를 도입하지 않습니다. 
 이름 대신 밑줄을 사용하는 것은 입력의 일부가 무시된다는 점을 독자에게 명확하게 전달하는 방법입니다.

```lean
def List.head? {α : Type} (xs : List α) : Option α :=
  match xs with
  | [] => none
  | y :: _ => some y
```

Lean 명명 규칙은 `Option`을 반환하는 버전에 대해 접미사 `?`, 잘못된 입력이 제공될 때 충돌하는 버전에 대해 `!`, 작업이 실패할 때 기본값을 반환하는 버전에 대해 `D` 접미사를 사용하여 그룹에서 실패할 수 있는 작업을 정의하는 것입니다. 
 이 패턴에 따라 `List.head`는 호출자에게 목록이 비어 있지 않다는 수학적 증거를 제공하도록 요구하고, `List.head?`는 `Option`을 반환하고, `List.head!`은 빈 목록이 전달되면 프로그램을 중단시키며, `List.headD`은 목록이 비어 있는 경우 반환할 기본값을 사용합니다. 
 물음표와 느낌표는 특수 구문이 아닌 이름의 일부입니다. Lean의 명명 규칙은 많은 언어보다 더 자유롭기 때문입니다.

`head?`은 `List` 네임스페이스에 정의되어 있으므로 접근자 표기법과 함께 사용할 수 있습니다.

```lean
#eval primesUnder10.head?
```

```text
some 2
```

그러나 빈 목록에서 테스트하려고 하면 두 가지 오류가 발생합니다.

```lean
#eval [].head?
```

```text
don't know how to synthesize implicit argument `α`
  @List.nil ?m.3
context:
⊢ Type ?u.71462
```

```text
don't know how to synthesize implicit argument `α`
  @_root_.List.head? ?m.3 []
context:
⊢ Type ?u.71462
```

이는 Lean이 표현식 타입을 완전히 결정할 수 없었기 때문입니다. 
 특히 `List.head?`에 대한 암시적 타입 인수나 `List.nil`에 대한 암시적 타입 인수를 찾을 수 없습니다. 
 Lean의 출력에서 ​​`?m.XYZ`는 추론할 수 없는 프로그램의 일부를 나타냅니다. 
 이러한 알 수 없는 부분을 _메타변수_라고 하며 일부 오류 메시지에서 발생합니다. 
 표현식을 평가하려면 Lean이 해당 타입을 찾을 수 있어야 하는데, 빈 목록에는 타입을 찾을 수 있는 항목이 없기 때문에 타입을 사용할 수 없습니다. 
 타입을 명시적으로 제공하면 Lean이 계속 진행할 수 있습니다.

```lean
#eval [].head? (α := Int)
```

```text
none
```

타입 주석을 사용하여 타입을 제공할 수도 있습니다.

```lean
#eval ([] : List Int).head?
```

```text
none
```

오류 메시지는 유용한 단서를 제공합니다. 
 두 메시지 모두 _same_ 메타변수를 사용하여 누락된 암시적 인수를 설명합니다. 이는 Lean이 솔루션의 실제 값을 결정할 수 없음에도 불구하고 누락된 두 조각이 솔루션을 공유할 것이라고 결정했음을 의미합니다.

## `Prod`

"Product"의 약자인 `Prod` 구조는 두 값을 결합하는 일반적인 방법입니다. 
 예를 들어, `Prod Nat String`에는 `Nat` 및 `String`이 포함됩니다. 
 즉, `PPoint Nat`은 `Prod Nat Nat`로 대체될 수 있습니다. 
 `Prod`은 C#의 튜플, Kotlin의 `Pair` 및 `Triple` 타입, C++의 `tuple` 타입과 매우 유사합니다. 
 도메인 용어를 사용하면 코드를 더 쉽게 읽을 수 있기 때문에 `Point`과 같은 간단한 경우에도 자체 구조를 정의하는 것이 많은 애플리케이션에 가장 적합합니다. 
 또한 구조 타입을 정의하면 서로 다른 도메인 개념에 서로 다른 타입을 할당하여 혼동을 방지함으로써 더 많은 오류를 포착하는 데 도움이 됩니다.

반면에 새로운 타입을 정의하는 오버헤드가 가치가 없는 경우도 있습니다. 
 또한 일부 라이브러리는 "쌍"보다 더 구체적인 개념이 없을 정도로 충분히 일반적입니다. 
 마지막으로 표준 라이브러리에는 내장된 쌍 타입 작업을 더 쉽게 해주는 다양한 편의 기능이 포함되어 있습니다.

`Prod` 구조는 두 가지 타입 인수로 정의됩니다.

```lean
structure Prod (α : Type) (β : Type) : Type where
  fst : α
  snd : β
```

목록은 너무 자주 사용되므로 더 읽기 쉽게 만드는 특별한 구문이 있습니다. 
 같은 이유로 제품 타입과 해당 생성자 모두 특수 구문을 갖습니다. 
 `Prod α β` 타입은 일반적으로 `α × β`로 작성되며 데카르트 집합의 곱에 대한 일반적인 표기법을 반영합니다. 
 마찬가지로 쌍에 대한 일반적인 수학적 표기법을 `Prod`에 사용할 수 있습니다. 
 즉, 다음과 같이 작성하는 대신:

```lean
def fives : String × Int := { fst := "five", snd := 5 }
```

다음과 같이 작성하면 충분합니다.

```lean
def fives : String × Int := ("five", 5)
```

두 표기법 모두 오른쪽 결합적입니다. 
 이는 다음 정의가 동일함을 의미합니다.

```lean
def sevens : String × Int × Nat := ("VII", 7, 4 + 3)
```

```lean
def sevens : String × (Int × Nat) := ("VII", (7, 4 + 3))
```

즉, 두 개 이상의 타입의 모든 제품과 해당 생성자는 실제로 내부적으로 중첩된 제품이자 중첩된 쌍입니다.

## `Sum`

`Sum` 데이터 타입은 서로 다른 두 타입의 값 중에서 선택할 수 있는 일반적인 방법입니다. 
 예를 들어, `Sum String Int`은 `String` 또는 `Int`입니다. 
 `Prod`와 마찬가지로 `Sum`은 매우 일반적인 코드를 작성할 때, 적절한 도메인별 타입이 없는 아주 작은 코드 섹션에 대해 또는 표준 라이브러리에 유용한 기능이 포함된 경우에 사용해야 합니다. 
 대부분의 상황에서는 맞춤형 귀납적 타입을 사용하는 것이 더 읽기 쉽고 유지 관리하기 쉽습니다.

`Sum α β` 타입의 값은 `α` 타입의 값에 적용된 생성자 `inl`이거나 `β` 타입의 값에 적용된 생성자 `inr`입니다.

```lean
inductive Sum (α : Type) (β : Type) : Type where
  | inl : α → Sum α β
  | inr : β → Sum α β
```

이 이름은 각각 "왼쪽 주입"과 "오른쪽 주입"의 약어입니다. 
 데카르트 곱 표기법이 `Prod`에 사용되는 것처럼 "원 안의 더하기" 표기법이 `Sum`에 사용되므로 `α ⊕ β`는 `Sum α β`을 쓰는 또 다른 방법입니다. 
 `Sum.inl` 및 `Sum.inr`에 대한 특별한 구문은 없습니다.

예를 들어 애완동물 이름이 개 이름이거나 고양이 이름일 수 있는 경우 해당 타입은 문자열 합계로 도입될 수 있습니다.

```lean
def PetName : Type := String ⊕ String
```

실제 프로그램에서는 일반적으로 유익한 생성자 이름을 사용하여 이 목적을 위한 사용자 정의 귀납적 데이터 타입을 정의하는 것이 더 좋습니다. 
 여기서 `Sum.inl`은 개 이름으로, `Sum.inr`은 고양이 이름으로 사용됩니다. 
 이러한 생성자는 동물 이름 목록을 작성하는 데 사용할 수 있습니다.

```lean
def animals : List PetName :=
  [Sum.inl "Spot", Sum.inr "Tiger", Sum.inl "Fifi",
   Sum.inl "Rex", Sum.inr "Floof"]
```

패턴 일치를 사용하여 두 생성자를 구별할 수 있습니다. 
 예를 들어, 동물 이름 목록에서 개 수(즉, `Sum.inl` 생성자의 수)를 계산하는 함수는 다음과 같습니다.

```lean
def howManyDogs (pets : List PetName) : Nat :=
  match pets with
  | [] => 0
  | Sum.inl _ :: morePets => howManyDogs morePets + 1
  | Sum.inr _ :: morePets => howManyDogs morePets
```

함수 호출은 중위 연산자보다 먼저 평가되므로 `howManyDogs morePets + 1`은 `(howManyDogs morePets) + 1`과 동일합니다. 
 예상대로 `#eval howManyDogs animals`는 `3`을 생성합니다.

## `Unit`

`Unit`은 `unit`이라는 인수 없는 생성자가 하나만 있는 타입입니다. 
 즉, 어떠한 인수도 적용되지 않은 해당 생성자로 구성된 단일 값만 설명합니다. 
 `Unit`은 다음과 같이 정의됩니다.

```lean
inductive Unit : Type where
  | unit : Unit
```

`Unit` 자체로는 특별히 유용하지 않습니다. 
 그러나 다형성 코드에서는 누락된 데이터에 대한 자리 표시자로 사용될 수 있습니다. 
 예를 들어, 다음 귀납적 데이터 타입은 산술 표현식을 나타냅니다.

```lean
inductive ArithExpr (ann : Type) : Type where
  | int : ann → Int → ArithExpr ann
  | plus : ann → ArithExpr ann → ArithExpr ann → ArithExpr ann
  | minus : ann → ArithExpr ann → ArithExpr ann → ArithExpr ann
  | times : ann → ArithExpr ann → ArithExpr ann → ArithExpr ann
```

타입 인수 `ann`은 주석을 나타내며 각 생성자에는 주석이 달려 있습니다. 
 파서에서 나오는 표현식에는 소스 위치가 주석으로 추가될 수 있으므로 `ArithExpr SourcePos` 반환 타입은 파서가 각 하위 표현식에 `SourcePos`을 넣도록 보장합니다. 
 그러나 파서에서 제공되지 않는 표현식에는 소스 위치가 없으므로 해당 타입은 `ArithExpr Unit`이 될 수 있습니다.

또한 모든 Lean 함수에는 인수가 있으므로 다른 언어의 인수가 없는 함수는 `Unit` 인수를 사용하는 함수로 표시될 수 있습니다. 
 반환 위치에서 `Unit` 타입은 C에서 파생된 언어의 `void`와 유사합니다. 
 C 계열에서 `void`을 반환하는 함수는 호출자에게 제어를 반환하지만 흥미로운 값을 반환하지 않습니다. 
 의도적으로 흥미롭지 않은 값이므로 `Unit`을 사용하면 타입 시스템에서 특수 목적의 `void` 기능을 요구하지 않고도 이를 표현할 수 있습니다. 
 유닛의 생성자는 빈 괄호(`() : Unit`)로 작성할 수 있습니다.

## `Empty`

`Empty` 데이터 타입에는 생성자가 전혀 없습니다. 
 따라서 일련의 호출이 `Empty` 타입의 값으로 종료될 수 없기 때문에 연결할 수 없는 코드를 나타냅니다.

`Empty`은 `Unit`만큼 자주 사용되지 않습니다. 
 그러나 일부 특수한 상황에서는 유용합니다. 
 많은 다형성 데이터 타입은 모든 생성자에서 모든 타입 인수를 사용하지 않습니다. 
 예를 들어, `Sum.inl` 및 `Sum.inr`은 각각 `Sum`의 타입 인수 중 하나만 사용합니다. 
 `Empty`을 `Sum`에 대한 타입 인수 중 하나로 사용하면 프로그램의 특정 지점에서 생성자 중 하나를 제외할 수 있습니다. 
 이를 통해 추가 제한 사항이 있는 컨텍스트에서 일반 코드를 사용할 수 있습니다.

## 이름 지정: 합계, 곱, 단위

일반적으로 여러 생성자를 제공하는 타입을 _sum 타입_이라고 하며, 단일 생성자가 여러 인수를 취하는 타입을 _제품 타입_이라고 합니다. 
 이 용어는 일반 산술에 사용되는 합계 및 곱과 관련이 있습니다. 
 관련된 타입에 유한 개수의 값이 포함되어 있을 때 관계를 가장 쉽게 확인할 수 있습니다. 
 `α` 및 `β`이 각각 $`n` 및 $`k` 고유 값을 포함하는 타입인 경우 `α ⊕ β`에는 $`n + k` 고유 값이 포함되고 `α × β`에는 $`n \times k` 고유 값이 포함됩니다. 
 예를 들어, `Bool`에는 `true` 및 `false`의 두 가지 값이 있고, `Unit`에는 `Unit.unit`라는 한 가지 값이 있습니다. 
 곱 `Bool × Unit`에는 `(true, Unit.unit)` 및 `(false, Unit.unit)`의 두 값이 있고 합계 `Bool ⊕ Unit`에는 `Sum.inl true`, `Sum.inl false` 및 `Sum.inr Unit.unit`의 세 값이 있습니다. 
 마찬가지로 $`2 \times 1 = 2` 및 $`2 + 1 = 3`입니다.

### 자주 만나는 메시지

모든 정의 가능한 구조 또는 귀납적 타입이 `Type` 타입을 가질 수 있는 것은 아닙니다. 
 특히 생성자가 임의의 타입을 인수로 사용하는 경우 귀납적 타입은 다른 타입을 가져야 합니다. 
 이러한 오류는 일반적으로 "우주 수준"에 관한 내용을 나타냅니다. 
 예를 들어, 이 귀납적 타입의 경우:

```lean
inductive MyType : Type where
  | ctor : (α : Type) → α → MyType
```

Lean은 다음과 같은 오류를 발생시킵니다.

```text
Invalid universe level in constructor `MyType.ctor`: Parameter `α` has type
  Type
at universe level
  2
which is not less than or equal to the inductive type's resulting universe level
  1
```

이후 장에서는 이것이 왜 발생하는지, 정의를 수정하여 작동하게 만드는 방법을 설명합니다. 
 지금은 생성자보다는 귀납적 타입 전체에 대한 인수로 타입을 만들어 보십시오.

마찬가지로 생성자의 인수가 정의 중인 데이터 타입을 인수로 사용하는 함수인 경우 정의가 거부됩니다. 
 예:

```lean
inductive MyType : Type where
  | ctor : (MyType → Int) → MyType
```

다음 메시지를 생성합니다.

```text
(kernel) arg #1 of 'MyType.ctor' has a non positive occurrence of the datatypes being declared
```

기술적인 이유로 이러한 데이터 타입을 허용하면 Lean의 내부 논리가 약화되어 정리 증명자로 사용하기에 부적합해질 수 있습니다.

두 개의 매개변수를 사용하는 재귀 함수는 쌍에 대해 일치해서는 안 되며 오히려 각 매개변수를 독립적으로 일치시켜야 합니다. 
 그렇지 않으면 더 작은 값에 대해 재귀 호출이 이루어졌는지 확인하는 Lean의 메커니즘이 재귀 호출의 입력 값과 인수 사이의 연결을 볼 수 없습니다. 
 예를 들어 두 목록의 길이가 동일한지 확인하는 이 함수는 거부됩니다.

```lean
def sameLength (xs : List α) (ys : List β) : Bool :=
  match (xs, ys) with
  | ([], []) => true
  | (x :: xs', y :: ys') => sameLength xs' ys'
  | _ => false
```

오류 메시지는 다음과 같습니다.

```text
fail to show termination for
  sameLength
with errors
failed to infer structural recursion:
Not considering parameter α of sameLength:
  it is unchanged in the recursive calls
Not considering parameter β of sameLength:
  it is unchanged in the recursive calls
Cannot use parameter xs:
  failed to eliminate recursive application
    sameLength xs' ys'
Cannot use parameter ys:
  failed to eliminate recursive application
    sameLength xs' ys'

Could not find a decreasing measure.
The basic measures relate at each recursive call as follows:
(<, ≤, =: relation proved, ? all proofs failed, _: no proof attempted)
              xs ys
1) 1760:28-46  ?  ?
Please use `termination_by` to specify a decreasing measure.
```

이 문제는 중첩된 패턴 일치를 통해 해결할 수 있습니다.

```lean
def sameLength (xs : List α) (ys : List β) : Bool :=
  match xs with
  | [] =>
    match ys with
    | [] => true
    | _ => false
  | x :: xs' =>
    match ys with
    | y :: ys' => sameLength xs' ys'
    | _ => false
```

다음 섹션에서 설명하는 동시 매칭은 종종 더 우아한 문제를 해결하는 또 다른 방법입니다.

귀납적 타입에 대한 논증을 잊어버리면 혼란스러운 메시지가 나올 수도 있습니다. 
 예를 들어, `α` 인수가 `ctor` 타입의 `MyType`에 전달되지 않은 경우:

```lean
inductive MyType (α : Type) : Type where
  | ctor : α → MyType
```

Lean은 다음 오류로 응답합니다.

```text
type expected, got
  (MyType : Type → Type)
```

오류 메시지는 `Type → Type`인 `MyType`의 타입 자체가 타입을 설명하지 않는다는 것을 의미합니다. 
 `MyType`에는 실제로 정직하고 선한 타입이 되려면 인수가 필요합니다.

정의에 대한 형식 서명과 같은 다른 컨텍스트에서 형식 인수가 생략되면 동일한 메시지가 나타날 수 있습니다.

```lean
inductive MyType (α : Type) : Type where
  | ctor : α → MyType α
```

```lean
def ofFive : MyType := ctor 5
```

```text
type expected, got
  (MyType : Type → Type)
```

다형성 타입을 사용하는 표현식을 평가하면 Lean이 값을 표시할 수 없는 상황이 발생할 수 있습니다. 
 `#eval` 명령은 결과 표시 방법을 결정하기 위해 표현식 타입을 사용하여 제공된 표현식을 평가합니다. 
 함수와 같은 일부 타입의 경우 이 프로세스가 실패하지만 Lean은 대부분의 다른 타입에 대한 표시 코드를 자동으로 생성할 수 있습니다. 
 예를 들어 Lean에 `WoodSplittingTool`에 대한 특정 표시 코드를 제공할 필요가 없습니다.```lean
inductive WoodSplittingTool where
  | axe
  | maul
  | froe
```
```lean
#eval WoodSplittingTool.axe
```
```text
WoodSplittingTool.axe
```그러나 여기서 Lean이 사용하는 자동화에는 제한이 있습니다. 
 `allTools`은 세 가지 도구의 목록입니다.```lean
def allTools : List WoodSplittingTool := [
  WoodSplittingTool.axe,
  WoodSplittingTool.maul,
  WoodSplittingTool.froe
]
```평가하면 오류가 발생합니다.```lean
#eval allTools
```
```text
could not synthesize a `ToExpr`, `Repr`, or `ToString` instance for type
  List WoodSplittingTool
```이는 Lean이 목록을 표시하기 위해 내장 테이블의 코드를 사용하려고 시도하지만 이 코드에서는 `WoodSplittingTool`에 대한 표시 코드가 이미 존재해야 하기 때문입니다. 
 이 오류는 데이터 타입이 정의될 때 마지막 순간에 `#eval`의 일부가 아닌 정의에 `deriving Repr`를 추가하여 이 표시 코드를 생성하도록 Lean에 지시함으로써 해결될 수 있습니다.```lean
inductive Firewood where
  | birch
  | pine
  | beech
deriving Repr
````Firewood` 목록 평가가 성공했습니다.```lean
def allFirewood : List Firewood := [
  Firewood.birch,
  Firewood.pine,
  Firewood.beech
]
```
```lean
#eval allFirewood
```
```text
[Firewood.birch, Firewood.pine, Firewood.beech]
```

### 연습문제

* 목록의 마지막 항목을 찾는 함수를 작성하세요. `Option`을(를) 반환해야 합니다. 
 * 주어진 조건을 만족하는 목록의 첫 번째 항목을 찾는 함수를 작성하세요. `def List.findFirst? {α : Type} (xs : List α) (predicate : α → Bool) : Option α := …`으로 정의를 시작하세요. 
 * 한 쌍의 두 필드를 서로 전환하는 `Prod.switch` 함수를 작성하세요. `def Prod.switch {α β : Type} (pair : α × β) : β × α := …`으로 정의를 시작하세요. 
 * 사용자 정의 데이터 타입을 사용하도록 `PetName` 예제를 다시 작성하고 이를 `Sum`을 사용하는 버전과 비교합니다. 
 * 두 개의 목록을 쌍의 목록으로 결합하는 함수 `zip`을 작성하세요. 결과 목록은 가장 짧은 입력 목록만큼 길어야 합니다. `def zip {α β : Type} (xs : List α) (ys : List β) : List (α × β) := …`으로 정의를 시작하세요. 
 * 목록의 첫 번째 $`n` 항목을 반환하는 다형성 함수 `take`을 작성하세요. 여기서 $`n`은 `Nat`입니다. 목록에 $`n` 미만의 항목이 포함된 경우 결과 목록은 전체 입력 목록이어야 합니다. `#eval take 3 ["bolete", "oyster"]`은 `["bolete", "oyster"]`을 생성하고 `#eval take 1 ["bolete", "oyster"]`는 `["bolete"]`을 생성해야 합니다. 
 * 타입과 산술 간의 비유를 사용하여 합계에 곱을 분배하는 함수를 작성합니다. 즉, `α × (β ⊕ γ) → (α × β) ⊕ (α × γ)` 타입이어야 합니다. 
 * 타입과 산술 간의 비유를 사용하여 2의 곱셈을 합으로 바꾸는 함수를 작성하세요. 즉, `Bool × α → α ⊕ α` 타입이어야 합니다.

Lean에는 프로그램을 훨씬 더 간결하게 만드는 다양한 편의 기능이 포함되어 있습니다.

### 자동 implicit 매개변수

Lean에서 다형성 함수를 작성할 때 일반적으로 모든 암시적 매개변수를 나열할 필요는 없습니다. 
 대신 간단히 언급할 수 있습니다. 
 Lean이 해당 타입을 결정할 수 있으면 자동으로 암시적 매개변수로 삽입됩니다. 
 즉, `length`의 이전 정의는 다음과 같습니다.

```lean
def length {α : Type} (xs : List α) : Nat :=
  match xs with
  | [] => 0
  | y :: ys => Nat.succ (length ys)
```

`{α : Type}` 없이 작성할 수 있습니다.

```lean
def length (xs : List α) : Nat :=
  match xs with
  | [] => 0
  | y :: ys => Nat.succ (length ys)
```

이는 많은 암시적 매개변수를 사용하는 고도로 다형성 정의를 크게 단순화할 수 있습니다.

### 패턴 매칭 정의

`def`으로 함수를 정의할 때 인수 이름을 지정하고 즉시 패턴 일치와 함께 사용하는 것이 일반적입니다. 
 예를 들어, `length`에서 `xs` 인수는 `match`에서만 사용됩니다. 
 이러한 상황에서는 인수 이름을 전혀 지정하지 않고 `match` 표현식의 사례를 직접 작성할 수 있습니다.

첫 번째 단계는 인수 타입을 콜론 오른쪽으로 이동하여 반환 타입이 함수 타입이 되도록 하는 것입니다. 
 예를 들어 `length`의 타입은 `List α → Nat`입니다. 
 그런 다음 `:=`를 패턴 일치의 각 사례로 바꿉니다.

```lean
def length : List α → Nat
  | [] => 0
  | y :: ys => Nat.succ (length ys)
```

이 구문은 둘 이상의 인수를 사용하는 함수를 정의하는 데에도 사용할 수 있습니다. 
 이 경우 패턴은 쉼표로 구분됩니다. 
 예를 들어 `drop`은 숫자 $`n`과 목록을 사용하고 첫 번째 $`n` 항목을 제거한 후 목록을 반환합니다.

```lean
def drop : Nat → List α → List α
  | Nat.zero, xs => xs
  | _, [] => []
  | Nat.succ n, x :: xs => drop n xs
```

명명된 인수와 패턴도 동일한 정의에서 사용할 수 있습니다. 
 예를 들어 기본값과 선택적 값을 취하고 선택적 값이 `none`일 때 기본값을 반환하는 함수는 다음과 같이 작성할 수 있습니다.

```lean
def fromOption (default : α) : Option α → α
  | none => default
  | some x => x
```

이 함수는 표준 라이브러리에서 `Option.getD`이라고 하며 점 표기법으로 호출할 수 있습니다.

```lean
#eval (some "salmonberry").getD ""
```

```text
"salmonberry"
```

```lean
#eval none.getD ""
```

```text
""
```

# 지역 정의

계산에서 중간 단계의 이름을 지정하는 것이 유용한 경우가 많습니다. 
 많은 경우 중간 값은 그 자체로 유용한 개념을 나타내며 명시적으로 이름을 지정하면 프로그램을 더 쉽게 읽을 수 있습니다. 
 다른 경우에는 중간 값이 두 번 이상 사용됩니다. 
 대부분의 다른 언어와 마찬가지로 Lean에서도 동일한 코드를 두 번 작성하면 두 번 계산되고, 결과를 변수에 저장하면 계산 결과가 저장되어 재사용됩니다.

예를 들어, `unzip`은 쌍 목록을 목록 쌍으로 변환하는 함수입니다. 
 쌍 목록이 비어 있으면 `unzip`의 결과는 빈 목록 쌍입니다. 
 쌍 목록의 머리 부분에 쌍이 있으면 목록의 나머지 부분을 압축 해제한 결과에 쌍의 두 필드가 추가됩니다. 
 `unzip`의 정의는 해당 설명을 정확히 따릅니다.

```lean
def unzip : List (α × β) → List α × List β
  | [] => ([], [])
  | (x, y) :: xys =>
    (x :: (unzip xys).fst, y :: (unzip xys).snd)
```

불행하게도 문제가 있습니다. 이 코드는 필요한 것보다 느립니다. 
 쌍 목록의 각 항목은 두 번의 재귀 호출로 이어지며, 이로 인해 이 함수는 기하급수적인 시간이 걸립니다. 
 그러나 두 재귀 호출 모두 동일한 결과를 가지므로 재귀 호출을 두 번 할 이유가 없습니다.

Lean에서는 재귀 호출의 결과에 `let`을 사용하여 이름을 지정하고 저장할 수 있습니다. 
 `let`을 사용한 로컬 정의는 `def`을 사용한 최상위 정의와 유사합니다. 즉, 로컬에서 정의할 이름, 원하는 경우 인수, 타입 서명, `:=` 다음에 나오는 본문을 사용합니다. 
 로컬 정의 다음에 로컬 정의를 사용할 수 있는 표현식(`let` 표현식의 _body_이라고 함)은 `let` 키워드보다 작거나 같은 파일의 열에서 시작하여 새 줄에 있어야 합니다. 
 `unzip`에 `let`이 포함된 로컬 정의는 다음과 같습니다.

```lean
def unzip : List (α × β) → List α × List β
  | [] => ([], [])
  | (x, y) :: xys =>
    let unzipped : List α × List β := unzip xys
    (x :: unzipped.fst, y :: unzipped.snd)
```

한 줄에 `let`을 사용하려면 세미콜론을 사용하여 본문과 로컬 정의를 구분하세요.

`let`을 사용한 로컬 정의는 하나의 패턴이 데이터 타입의 모든 사례와 일치하기에 충분할 때 패턴 일치를 사용할 수도 있습니다. 
 `unzip`의 경우 재귀 호출의 결과는 쌍입니다. 
 쌍에는 단일 생성자만 있으므로 `unzipped` 이름을 쌍 패턴으로 바꿀 수 있습니다.

```lean
def unzip : List (α × β) → List α × List β
  | [] => ([], [])
  | (x, y) :: xys =>
    let (xs, ys) : List α × List β := unzip xys
    (x :: xs, y :: ys)
```

`let`과 함께 패턴을 현명하게 사용하면 접근자 호출을 직접 작성하는 것에 비해 코드를 더 쉽게 읽을 수 있습니다.

`let`과 `def`의 가장 큰 차이점은 재귀적 `let` 정의는 `let rec`을 작성하여 명시적으로 표시해야 한다는 것입니다. 
 예를 들어 목록을 뒤집는 한 가지 방법은 다음 정의와 같이 재귀 도우미 함수를 사용하는 것입니다.

```lean
def reverse (xs : List α) : List α :=
  let rec helper : List α → List α → List α
    | [], soFar => soFar
    | y :: ys, soFar => helper ys (y :: soFar)
  helper xs []
```

도우미 함수는 입력 목록을 따라 한 번에 한 항목씩 `soFar`로 이동합니다. 
 입력 목록의 끝에 도달하면 `soFar`에는 입력의 반전된 버전이 포함됩니다.

#### 타입 추론

많은 상황에서 Lean은 표현식 타입을 자동으로 결정할 수 있습니다. 
 이러한 경우 명시적 타입은 최상위 정의(`def` 사용)와 로컬 정의(`let` 사용) 모두에서 생략될 수 있습니다. 
 예를 들어 `unzip`에 대한 재귀 호출에는 주석이 필요하지 않습니다.

```lean
def unzip : List (α × β) → List α × List β
  | [] => ([], [])
  | (x, y) :: xys =>
    let unzipped := unzip xys
    (x :: unzipped.fst, y :: unzipped.snd)
```

경험상 리터럴 값 타입(예: 문자열 및 숫자)을 생략하는 것이 일반적으로 효과적이지만 Lean은 의도한 타입보다 더 구체적인 리터럴 숫자 타입을 선택할 수 있습니다. 
 Lean은 인수 타입과 반환 타입을 이미 알고 있기 때문에 일반적으로 함수 응용 프로그램의 타입을 결정할 수 있습니다. 
 함수 정의에 대한 반환 타입을 생략하면 대개 작동하지만 함수 매개변수에는 일반적으로 주석이 필요합니다. 
 예제의 `unzipped`과 같이 함수가 아닌 정의는 해당 본문에 타입 주석이 필요하지 않고 이 정의의 본문이 함수 애플리케이션인 경우 타입 주석이 필요하지 않습니다.

명시적인 `match` 표현식을 사용하는 경우 `unzip`에 대한 반환 타입을 생략할 수 있습니다.

```lean
def unzip (pairs : List (α × β)) :=
  match pairs with
  | [] => ([], [])
  | (x, y) :: xys =>
    let unzipped := unzip xys
    (x :: unzipped.fst, y :: unzipped.snd)
```

일반적으로 말해서, 타입 주석이 너무 적지 않고 너무 많으면 오류를 범하는 것이 좋습니다. 
 우선 명시적 타입은 코드에 대한 가정을 독자에게 전달합니다. 
 Lean이 자체적으로 타입을 결정할 수 있더라도 Lean에 타입 정보를 반복적으로 쿼리하지 않고도 코드를 읽는 것이 더 쉬울 수 있습니다. 
 둘째, 명시적 타입은 오류를 현지화하는 데 도움이 됩니다. 
 프로그램의 타입이 더 명확할수록 오류 메시지는 더 많은 정보를 제공할 수 있습니다. 
 이는 매우 표현력이 뛰어난 타입 시스템을 갖춘 Lean과 같은 언어에서 특히 중요합니다. 
 셋째, 명시적 타입을 사용하면 처음부터 프로그램 작성이 더 쉬워집니다. 
 타입은 사양이며, 컴파일러의 피드백은 사양을 충족하는 프로그램을 작성하는 데 유용한 도구가 될 수 있습니다. 
 마지막으로 Lean의 타입 추론은 최선의 노력 시스템입니다. 
 Lean의 타입 시스템은 매우 표현력이 풍부하기 때문에 모든 표현에 대해 찾을 수 있는 "최적" 또는 가장 일반적인 타입은 없습니다. 
 이는 타입을 얻더라도 해당 애플리케이션에 대해 그것이 _올바른_ 타입이라는 보장이 없다는 것을 의미합니다. 
 예를 들어 `14`은 `Nat` 또는 `Int`일 수 있습니다.

```lean
#check 14
```

```text
14 : Nat
```

```lean
#check (14 : Int)
```

```text
14 : Int
```

타입 주석이 누락되면 혼란스러운 오류 메시지가 나타날 수 있습니다. 
 `unzip` 정의에서 모든 타입을 생략합니다.

```lean
def unzip pairs :=
  match pairs with
  | [] => ([], [])
  | (x, y) :: xys =>
    let unzipped := unzip xys
    (x :: unzipped.fst, y :: unzipped.snd)
```

`match` 표현식에 대한 메시지로 이어집니다.

```text
Invalid match expression: This pattern contains metavariables:
  []
```

`match`은 검사 중인 값의 타입을 알아야 하는데 해당 타입을 사용할 수 없기 때문입니다. 
 "메타변수"는 오류 메시지에 `?m.XYZ`로 쓰여진 프로그램의 알 수 없는 부분입니다. 이에 대해서는 다형성 섹션에 설명되어 있습니다. 
 이 프로그램에서는 인수에 대한 타입 주석이 필요합니다.

일부 매우 간단한 프로그램에도 타입 주석이 필요합니다. 
 예를 들어, 항등 함수는 전달된 인수가 무엇이든 반환합니다. 
 인수 및 타입 주석을 사용하면 다음과 같습니다.

```lean
def id (x : α) : α := x
```

Lean은 자체적으로 반환 타입을 결정할 수 있습니다.

```lean
def id (x : α) := x
```

그러나 인수 타입을 생략하면 오류가 발생합니다.

```lean
def id x := x
```

```text
Failed to infer type of binder `x`
```

일반적으로 "추론 실패"와 같은 메시지나 메타변수를 언급하는 메시지는 더 많은 타입 주석이 필요하다는 신호인 경우가 많습니다. 
 특히 Lean을 학습하는 동안 대부분의 타입을 명시적으로 제공하는 것이 유용합니다.

# 동시 매칭

패턴 일치 정의와 마찬가지로 패턴 일치 표현식은 한 번에 여러 값을 일치시킬 수 있습니다. 
 검사할 표현식과 일치하는 패턴은 정의에 사용된 구문과 유사하게 둘 사이에 쉼표를 사용하여 작성됩니다. 
 다음은 동시 일치를 사용하는 `drop` 버전입니다.

```lean
def drop (n : Nat) (xs : List α) : List α :=
  match n, xs with
  | Nat.zero, ys => ys
  | _, [] => []
  | Nat.succ n , y :: ys => drop n ys
```

동시 매칭은 쌍 매칭과 유사하지만 중요한 차이점이 있습니다. 
 Lean은 일치하는 표현식과 패턴 사이의 연결을 추적하며 이 정보는 종료 확인 및 정적 타입 정보 전파를 포함하는 목적으로 사용됩니다. 
 결과적으로, `xs`과 `x :: xs'` 사이의 연결이 중간 쌍에 의해 모호해지기 때문에 쌍과 일치하는 `sameLength` 버전이 종료 검사기에 의해 거부됩니다.

```lean
def sameLength (xs : List α) (ys : List β) : Bool :=
  match (xs, ys) with
  | ([], []) => true
  | (x :: xs', y :: ys') => sameLength xs' ys'
  | _ => false
```

```text
fail to show termination for
  sameLength
with errors
failed to infer structural recursion:
Not considering parameter α of sameLength:
  it is unchanged in the recursive calls
Not considering parameter β of sameLength:
  it is unchanged in the recursive calls
Cannot use parameter xs:
  failed to eliminate recursive application
    sameLength xs' ys'
Cannot use parameter ys:
  failed to eliminate recursive application
    sameLength xs' ys'

Could not find a decreasing measure.
The basic measures relate at each recursive call as follows:
(<, ≤, =: relation proved, ? all proofs failed, _: no proof attempted)
              xs ys
1) 1748:28-46  ?  ?
Please use `termination_by` to specify a decreasing measure.
```

두 목록을 동시에 일치시키는 것이 허용됩니다.

```lean
def sameLength (xs : List α) (ys : List β) : Bool :=
  match xs, ys with
  | [], [] => true
  | x :: xs', y :: ys' => sameLength xs' ys'
  | _, _ => false
```

# 자연수 패턴

데이터 타입 및 패턴 섹션에서 `even`은 다음과 같이 정의되었습니다.

```lean
def even (n : Nat) : Bool :=
  match n with
  | Nat.zero => true
  | Nat.succ k => not (even k)
```

`List.cons` 및 `List.nil`을 직접 사용하는 것보다 목록 패턴을 더 읽기 쉽게 만드는 특수 구문이 있는 것처럼 리터럴 숫자와 `+`을 사용하여 자연수를 일치시킬 수 있습니다. 
 예를 들어 `even`은 다음과 같이 정의할 수도 있습니다.

```lean
def even : Nat → Bool
  | 0 => true
  | n + 1 => not (even n)
```

이 표기법에서 `+` 패턴에 대한 인수는 다른 역할을 합니다. 
 뒤에서 왼쪽 인수(위의 `n`)는 일부 `Nat.succ` 패턴에 대한 인수가 되고, 오른쪽 인수(위의 `1`)는 패턴을 둘러쌀 `Nat.succ`의 수를 결정합니다. 
 `Nat`을 2로 나누고 나머지를 삭제하는 `halve`의 명시적 패턴:

```lean
def halve : Nat → Nat
  | Nat.zero => 0
  | Nat.succ Nat.zero => 0
  | Nat.succ (Nat.succ n) => halve n + 1
```

숫자 리터럴과 `+`로 대체될 수 있습니다.

```lean
def halve : Nat → Nat
  | 0 => 0
  | 1 => 0
  | n + 2 => halve n + 1
```

이면에서는 두 정의가 완전히 동일합니다. 
 기억하세요: `halve n + 1`은 `halve (n + 1)`가 아니라 `(halve n) + 1`과 동일합니다.

이 구문을 사용할 때 `+`에 대한 두 번째 인수는 항상 리터럴 `Nat`이어야 합니다. 
 덧셈은 교환 가능하지만 패턴에서 인수를 뒤집으면 다음과 같은 오류가 발생할 수 있습니다.

```lean
def halve : Nat → Nat
  | 0 => 0
  | 1 => 0
  | 2 + n => halve n + 1
```

```text
Invalid pattern(s): `n` is an explicit pattern variable, but it only occurs in positions that are inaccessible to pattern matching:
  .(Nat.add 2 n)
```

이러한 제한을 통해 Lean은 패턴에서 `+` 표기법의 모든 사용을 기본 `Nat.succ`의 사용으로 변환하여 뒤에서 언어를 더 단순하게 유지할 수 있습니다.

# 익명 함수

Lean의 기능은 최상위 수준에서 정의될 필요가 없습니다. 
 표현식으로서 함수는 `fun` 구문으로 생성됩니다. 
 함수 표현식은 `fun` 키워드로 시작하고 그 뒤에 하나 이상의 매개변수가 옵니다. 이 매개변수는 `=>`를 사용하여 반환 표현식과 구분됩니다. 
 예를 들어 숫자에 1을 더하는 함수는 다음과 같이 작성할 수 있습니다.

```lean
#check fun x => x + 1
```

```text
fun x => x + 1 : Nat → Nat
```

타입 주석은 괄호와 콜론을 사용하여 `def`과 동일한 방식으로 작성됩니다.

```lean
#check fun (x : Int) => x + 1
```

```text
fun x => x + 1 : Int → Int
```

마찬가지로 암시적 매개변수는 중괄호를 사용하여 작성할 수 있습니다.

```lean
#check fun {α : Type} (x : α) => x
```

```text
fun {α} x => x : {α : Type} → α → α
```

프로그래밍 언어의 수학적 설명에 사용되는 일반적인 표기법은 Lean이 키워드 `fun`을 갖는 그리스 문자 람다(lambda)를 사용하기 때문에 이러한 스타일의 익명 함수 표현을 종종 _람다 표현_이라고 합니다. 
 Lean에서는 `fun` 대신 `λ`을 사용하는 것을 허용하지만 `fun`을 작성하는 것이 가장 일반적입니다.

익명 함수는 `def`에서 사용되는 다중 패턴 스타일도 지원합니다. 
 예를 들어, 자연수가 존재하는 경우 자연수의 선행자를 반환하는 함수는 다음과 같이 작성할 수 있습니다.

```lean
#check fun
  | 0 => none
  | n + 1 => some n
```

```text
fun x =>
  match x with
  | 0 => none
  | n.succ => some n : Nat → Option Nat
```

함수에 대한 Lean의 자체 설명에는 명명된 인수와 `match` 표현식이 있습니다. 
 Lean의 편리한 구문 단축어 중 다수는 배후에서 더 간단한 구문으로 확장되며 추상화가 때때로 누출됩니다.

인수를 사용하는 `def`을 사용하는 정의는 함수 표현식으로 다시 작성될 수 있습니다. 
 예를 들어 인수를 두 배로 늘리는 함수는 다음과 같이 작성할 수 있습니다.

```lean
def double : Nat → Nat := fun
  | 0 => 0
  | k + 1 => double k + 2
```

`fun x => x + 1`처럼 익명 함수가 매우 간단한 경우 함수를 생성하는 구문이 상당히 장황해질 수 있습니다. 
 해당 특정 예에서는 공백이 아닌 문자 6개가 함수를 소개하는 데 사용되었으며 본문은 공백이 아닌 문자 3개로만 구성됩니다. 
 이러한 간단한 경우에 대해 Lean은 속기를 제공합니다. 
 괄호로 묶인 표현식에서 가운데 ​​점 문자 `·`은 매개변수를 나타낼 수 있으며, 괄호 안의 표현식은 함수의 본문이 됩니다. 
 해당 특정 함수는 `(· + 1)`로 작성할 수도 있습니다.

중앙에 있는 점은 항상 _가장 가까운_ 주변 괄호 세트에서 함수를 생성합니다. 
 예를 들어, `(· + 5, 3)`은 숫자 쌍을 반환하는 함수이고, `((· + 5), 3)`은 함수와 숫자의 쌍입니다. 
 여러 점이 사용되면 왼쪽에서 오른쪽으로 매개변수가 됩니다.

```lean
(· , ·) 1 2
===>
(1, ·) 2
===>
(1, 2)
```

익명 함수는 `def` 또는 `let`을 사용하여 정의된 함수와 정확히 동일한 방식으로 적용될 수 있습니다. 
 `#eval (fun x => x + x) 5` 명령의 결과는 다음과 같습니다.

```text
10
```

`#eval (· * 2) 5`의 결과는 다음과 같습니다.

```text
10
```

# 네임스페이스

Lean의 각 이름은 이름 모음인 _namespace_에서 발생합니다. 
 이름은 `.`을 사용하여 네임스페이스에 배치되므로 `List.map`은 `List` 네임스페이스의 이름 `map`입니다. 
 서로 다른 네임스페이스의 이름은 동일하더라도 서로 충돌하지 않습니다. 
 이는 `List.map`과 `Array.map`이 다른 이름임을 의미합니다. 
 네임스페이스는 중첩될 수 있으므로 `Project.Frontend.User.loginTime`은 중첩된 네임스페이스 `Project.Frontend.User`의 이름 `loginTime`입니다.

이름은 네임스페이스 내에서 직접 정의할 수 있습니다. 
 예를 들어 `double`이라는 이름은 `Nat` 네임스페이스에 정의될 수 있습니다.

```lean
def Nat.double (x : Nat) : Nat := x + x
```

`Nat`은 타입의 이름이기도 하므로 `Nat` 타입의 표현식에서 `Nat.double`을 호출하는 데 점 표기법을 사용할 수 있습니다.

```lean
#eval (4 : Nat).double
```

```text
8
```

네임스페이스에서 직접 이름을 정의하는 것 외에도 `namespace` 및 `end` 명령을 사용하여 일련의 선언을 네임스페이스에 배치할 수 있습니다. 
 예를 들어, 이는 `NewNamespace` 네임스페이스에서 `triple` 및 `quadruple`을 정의합니다.

```lean
namespace NewNamespace
def triple (x : Nat) : Nat := 3 * x
def quadruple (x : Nat) : Nat := 2 * x + 2 * x
end NewNamespace
```

이를 참조하려면 이름 앞에 `NewNamespace.`을 붙입니다.

```lean
#check NewNamespace.triple
```

```text
NewNamespace.triple (x : Nat) : Nat
```

```lean
#check NewNamespace.quadruple
```

```text
NewNamespace.quadruple (x : Nat) : Nat
```

네임스페이스는 _개방_될 수 있으며, 이는 명시적인 한정 없이 이름을 사용할 수 있도록 허용합니다. 
 표현식 앞에 `open` `MyNamespace ``in`을 쓰면 `MyNamespace`의 내용을 표현식에서 사용할 수 있습니다. 
 예를 들어 `timesTwelve`는 `NewNamespace`을 연 후 `quadruple` 및 `triple`을 모두 사용합니다.

```lean
def timesTwelve (x : Nat) :=
  quadruple (triple x)
```

네임스페이스는 명령 이전에 열릴 수도 있습니다. 
 이를 통해 명령의 모든 부분이 단일 표현식이 아닌 네임스페이스의 내용을 참조할 수 있습니다. 
 이렇게 하려면 명령 앞에 `open`﻿` ... ``in`을 배치합니다.

```lean
#check quadruple
```

```text
NewNamespace.quadruple (x : Nat) : Nat
```

함수 서명은 이름의 전체 네임스페이스를 표시합니다. 
 네임스페이스는 파일의 나머지 부분에 대한 다음 명령에 따라 _모든_에 대해 추가로 열릴 수 있습니다. 
 이렇게 하려면 `open`의 최상위 사용법에서 `in`을 생략하면 됩니다.

# `if let`

합계 타입이 있는 값을 사용할 때 단일 생성자에만 관심이 있는 경우가 종종 있습니다. 
 예를 들어 Markdown 인라인 요소의 하위 집합을 나타내는 다음 타입이 제공됩니다.

```lean
inductive Inline : Type where
  | lineBreak
  | string : String → Inline
  | emph : Inline → Inline
  | strong : Inline → Inline
```

문자열 요소를 인식하고 그 내용을 추출하는 함수는 다음과 같이 작성할 수 있습니다.

```lean
def Inline.string? (inline : Inline) : Option String :=
  match inline with
  | Inline.string s => some s
  | _ => none
```

이 함수 본문을 작성하는 다른 방법은 `let`과 함께 `if`을 사용하는 것입니다.

```lean
def Inline.string? (inline : Inline) : Option String :=
  if let Inline.string s := inline then
    some s
  else none
```

이는 패턴 일치 `let` 구문과 매우 유사합니다. 
 차이점은 `else` 경우 fallback이 제공되기 때문에 합계 타입과 함께 사용할 수 있다는 것입니다. 
 일부 상황에서는 `match` 대신 `if let`을 사용하면 코드를 더 쉽게 읽을 수 있습니다.

# 위치 구조 인수

구조에 대한 섹션에서는 구조를 구성하는 두 가지 방법을 제시합니다. 
 1. `Point.mk 1 2`에서와 같이 생성자를 직접 호출할 수 있습니다. 
 2. `{ x := 1, y := 2 }`과 같이 중괄호 표기법을 사용할 수 있습니다.

일부 상황에서는 생성자 이름을 직접 지정하지 않고 이름 대신 위치적으로 인수를 전달하는 것이 편리할 수 있습니다. 
 예를 들어 다양한 유사한 구조 타입을 정의하면 도메인 개념을 분리하는 데 도움이 될 수 있지만 코드를 읽는 자연스러운 방법은 각 개념을 본질적으로 튜플로 처리할 수 있습니다. 
 이러한 컨텍스트에서는 인수를 꺾쇠 괄호 `⟨` 및 `⟩`로 묶을 수 있습니다. 
 `Point`는 `⟨1, 2⟩`로 쓸 수 있습니다. 
 조심하세요! 
 보다 작음 기호 `<` 및 보다 큼 기호 `>`처럼 보이지만 이 괄호는 다릅니다. 
 각각 `\<` 및 `\>`을 사용하여 입력할 수 있습니다.

명명된 생성자 인수에 대한 중괄호 표기와 마찬가지로 이 위치 구문은 Lean이 타입 주석이나 프로그램의 다른 타입 정보로부터 구조의 타입을 결정할 수 있는 컨텍스트에서만 사용할 수 있습니다. 
 예를 들어 `#eval ⟨1, 2⟩`은 다음 오류를 생성합니다.

```text
Invalid `⟨...⟩` notation: The expected type of this term could not be determined
```

이 오류는 사용 가능한 타입 정보가 없기 때문에 발생합니다. 
 `#eval (⟨1, 2⟩ : Point)`과 같은 주석을 추가하면 문제가 해결됩니다.

```text
{ x := 1.000000, y := 2.000000 }
```

# 문자열 보간

Lean에서는 문자열 앞에 `s!`을 붙이면 _보간_이 트리거됩니다. 여기서 문자열 내부의 중괄호 안에 포함된 표현식은 해당 값으로 대체됩니다. 
 이는 Python의 `f`-문자열 및 C#의 `$`-접두사가 붙은 문자열과 유사합니다. 
 예를 들어,

```lean
#eval s!"three fives is {NewNamespace.triple 5}"
```

출력을 산출합니다

```text
"three fives is 15"
```

모든 표현식을 문자열에 삽입할 수 있는 것은 아닙니다. 
 예를 들어, 함수를 보간하려고 시도하면 오류가 발생합니다.

```lean
#check s!"three fives is {NewNamespace.triple}"
```

오류가 발생합니다

```text
failed to synthesize
  ToString (Nat → Nat)

Hint: Additional diagnostic information may be available using the `set_option diagnostics true` command.
```

이는 함수를 문자열로 변환하는 표준 방법이 없기 때문입니다. 
 컴파일러가 다양한 타입의 표현식 평가 결과를 표시하는 방법을 설명하는 테이블을 유지 관리하는 것처럼 다양한 타입의 값을 문자열로 변환하는 방법을 설명하는 테이블을 유지 관리합니다. 
 `failed to synthesize instance` 메시지는 Lean 컴파일러가 이 테이블에서 해당 타입에 대한 항목을 찾지 못했음을 의미합니다. 
 타입 클래스에 관한 장에서는 테이블에 새 항목을 추가하는 방법을 포함하여 이 메커니즘을 더 자세히 설명합니다.

## 표현식 평가

Lean에서는 표현식이 평가될 때 계산이 발생합니다. 
 이는 수학 표현식의 일반적인 규칙을 따릅니다. 하위 표현식은 전체 표현식이 값이 될 때까지 일반적인 연산 순서에 따라 해당 값으로 대체됩니다. 
 `if` 또는 `match`을 평가할 때 분기의 표현식은 조건 값이나 일치 제목을 찾을 때까지 평가되지 않습니다.

변수에 값이 주어지면 변수는 절대 변경되지 않습니다. 
 수학과 유사하지만 대부분의 프로그래밍 언어와는 달리 Lean 변수는 새 값을 쓸 수 있는 주소가 아니라 단순히 값에 대한 자리 표시자입니다. 
 변수의 값은 `def`이 있는 전역 정의, `let`이 있는 로컬 정의, 함수에 대한 명명된 인수 또는 패턴 일치에서 나올 수 있습니다.

## 함수

Lean의 함수는 일급 값입니다. 즉, 다른 함수에 인수로 전달되고 변수에 저장되며 다른 값처럼 사용될 수 있습니다. 
 모든 Lean 함수는 정확히 하나의 인수를 취합니다. 
 둘 이상의 인수를 사용하는 함수를 인코딩하기 위해 Lean은 커링이라는 기술을 사용합니다. 여기서 첫 번째 인수를 제공하면 나머지 인수를 예상하는 함수가 반환됩니다. 
 인수가 없는 함수를 인코딩하기 위해 Lean은 정보가 가장 적은 인수인 `Unit` 타입을 사용합니다.

함수를 생성하는 세 가지 기본 방법은 다음과 같습니다. 
 1. 익명 함수는 `fun`을 사용하여 작성됩니다. 
 예를 들어, `Point`의 필드를 바꾸는 함수는 `fun (point : Point) => { x := point.y, y := point.x : Point }` 
 2로 작성할 수 있습니다. 매우 간단한 익명 함수는 괄호 안에 하나 이상의 중앙 점 `·`을 배치하여 작성됩니다. 
 중앙에 있는 각 점은 함수에 대한 인수가 되며 괄호는 해당 본문을 구분합니다. 
 예를 들어, 인수에서 1을 빼는 함수는 `fun x => x - 1` 대신 `(· - 1)`로 작성할 수 있습니다. 
 3. 함수는 인수 목록을 추가하거나 패턴 일치 표기법을 사용하여 `def` 또는 `let`을 사용하여 정의할 수 있습니다.

## 타입

Lean은 모든 표현식에 타입이 있는지 확인합니다. `Int`, `Point`, `{α : Type} → Nat → α → List α` 및 `Option (String ⊕ (Nat × String))`과 같은 
 타입은 표현식에 대해 최종적으로 발견될 수 있는 값을 설명합니다. 
 다른 언어와 마찬가지로 Lean의 타입은 Lean 컴파일러에서 확인하는 프로그램에 대한 경량 사양을 표현할 수 있으므로 특정 클래스의 단위 테스트가 필요하지 않습니다. 
 대부분의 언어와 달리 Lean의 타입은 프로그래밍 및 정리 증명의 세계를 통합하여 임의의 수학을 표현할 수도 있습니다. 
 정리를 증명하기 위해 Lean을 사용하는 것은 대부분 이 책의 범위를 벗어나지만 _[Theorem Proving in Lean 4](https://leanprover.github.io/theorem_proving_in_lean4/)_에는 이 주제에 대한 더 많은 정보가 포함되어 있습니다.

일부 표현식에는 여러 타입이 제공될 수 있습니다. 
 예를 들어 `3`은 `Int` 또는 `Nat`일 수 있습니다. 
 Lean에서 이는 동일한 것에 대한 두 가지 다른 타입이 아니라 동일한 방식으로 작성된 `Nat` 타입과 `Int` 타입의 두 가지 별도 표현식으로 이해되어야 합니다.

Lean은 때때로 타입을 자동으로 결정할 수 있지만 타입은 사용자가 제공해야 하는 경우가 많습니다. 
 이는 Lean의 타입 시스템이 매우 표현력이 풍부하기 때문입니다. 
 Lean이 타입을 찾을 수 있더라도 원하는 타입을 찾지 못할 수 있습니다. `3`은 `Int`로 사용되도록 의도될 수 있지만 Lean은 추가 제약 조건이 없으면 타입 `Nat`을 제공합니다. 
 일반적으로 대부분의 타입을 명시적으로 작성하고 Lean이 매우 명확한 타입만 채우도록 하는 것이 좋습니다. 
 이는 Lean의 오류 메시지를 개선하고 프로그래머의 의도를 더욱 명확하게 만드는 데 도움이 됩니다.

일부 함수나 데이터 타입은 타입을 인수로 사용합니다. 
 그것들은 _다형성_이라고 불립니다. 
 다형성은 목록에 있는 항목의 타입을 고려하지 않고 목록의 길이를 계산하는 것과 같은 프로그램을 허용합니다. 
 타입은 Lean에서 일류이기 때문에 다형성에는 특별한 구문이 필요하지 않으므로 타입은 다른 인수처럼 전달됩니다. 
 함수 타입에서 인수 이름을 지정하면 이후 타입에서 해당 이름을 언급할 수 있으며, 함수가 인수에 적용될 때 인수 이름을 적용된 실제 값으로 대체하여 결과 용어의 타입을 찾습니다.

## 구조체와 귀납적 타입

`structure` 또는 `inductive` 기능을 사용하여 새로운 데이터 타입을 Lean에 도입할 수 있습니다. 
 이러한 새로운 타입은 정의가 동일하더라도 다른 타입과 동등한 것으로 간주되지 않습니다. 
 데이터 타입에는 해당 값을 구성할 수 있는 방법을 설명하는 _생성자_가 있으며, 각 생성자는 몇 가지 인수를 사용합니다. 
 Lean의 생성자는 객체 지향 언어의 생성자와 동일하지 않습니다. Lean의 생성자는 할당된 객체를 초기화하는 활성 코드가 아니라 데이터의 비활성 보유자입니다.

일반적으로 `structure`은 제품 타입(즉, 여러 인수를 취하는 생성자가 하나만 있는 타입)을 소개하는 데 사용되는 반면, `inductive`은 합계 타입(즉, 고유한 생성자가 많은 타입)을 소개하는 데 사용됩니다. 
 `structure`로 정의된 데이터 타입에는 각 필드에 대해 하나의 접근자 함수가 제공됩니다. 
 구조와 귀납적 데이터 타입 모두 패턴 일치를 통해 소비될 수 있습니다. 이는 생성자를 호출하는 데 사용되는 구문의 하위 집합을 사용하여 생성자 내부에 저장된 값을 노출합니다. 
 패턴 일치는 가치를 생성하는 방법을 아는 것이 이를 소비하는 방법을 아는 것을 의미합니다.

# 재귀

정의되는 이름이 정의 자체에서 사용될 때 정의는 재귀적입니다. 
 Lean은 프로그래밍 언어일 뿐만 아니라 대화형 정리 증명이기 때문에 재귀 정의에 특정 제한 사항이 적용됩니다. 
 Lean의 논리적 측면에서 순환 정의는 논리적 불일치로 이어질 수 있습니다.

재귀적 정의가 Lean의 논리적 측면을 훼손하지 않도록 하기 위해 Lean은 호출되는 인수에 관계없이 모든 재귀 함수가 종료된다는 것을 증명할 수 있어야 합니다. 
 실제로 이는 재귀 호출이 구조적으로 더 작은 입력 부분에서 모두 수행되어 항상 기본 사례를 향한 진행이 보장되거나 사용자가 함수가 항상 종료된다는 다른 증거를 제공해야 함을 의미합니다. 
 마찬가지로, 재귀 귀납적 타입에는 해당 타입에서_ 함수를 인수로 취하는 생성자가 허용되지 않습니다. 이렇게 하면 종료되지 않는 함수를 인코딩할 수 있기 때문입니다.


## 장말 해설

### 핵심 개념 요약
- 에디터 중심 상호작용으로 Lean 코드를 평가하고 타입 정보를 읽는 기본 흐름을 다룹니다.
- 표현식 평가, 타입 확인, 함수/자료형/패턴 매칭의 기초를 단계적으로 연결합니다.
- REPL 중심 언어와 다른 Lean의 개발 피드백 루프를 체감하도록 구성되어 있습니다.

### 학습 포인트
1. 각 코드 조각을 에디터에서 직접 실행해 메시지와 타입 정보를 즉시 확인하는 습관이 중요합니다.
2. 문법 암기보다 평가 과정과 타입 추론 과정을 눈으로 추적하는 것이 학습 속도를 높입니다.

## 라이선스 및 변경 고지

이 번역 포스트는 원저작물의 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) 라이선스를 따릅니다. 원문의 의미를 보존하도록 번역했으며, 이해를 돕기 위해 장말 해설을 추가했습니다.
