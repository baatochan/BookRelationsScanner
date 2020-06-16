<template>
  <div>
    <p style="text-align: center">
      Wczytywanie tekstu możliwe jest po wpisaniu go ręcznie lub poprzez
      wczytanie pliku. <br />
      Program obsługuje pliki tekstowe w następujących formatach: *.txt,
      *.pdf.<br />
      Plik *.pdf musi zawierać tekst, czytanie tekstu z obrazów (OCR) nie jest
      wspierane.<br />
      Po załadowaniu tekstu możliwa jest jego edycja.<br />
      Dane zwracane z przeanalizowanego tekstu zwracają wagi połączeń pomiędzy
      bytami oraz liczbę wystąpień postaci.<br />
      Użytkownik posiada możliwość ręcznego złączenia dwóch bytów w jeden.
      <br />
      Funkcjonalność ta jest przydatna w przypadku gdy jedenbyt zostanie błędnie
      rozróżniony jako dwa osobne. <br />
      Wszelkie zmiany dokonane przez użytkownika mogą zostać przywrócone
      przyciskiem Przywróć zmiany.<br />
    </p>
  </div>
</template>

<script>
export default {};
</script>
