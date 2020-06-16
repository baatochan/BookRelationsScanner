<template>
  <div>
    <br />
    <h3 style="text-align: justify">
      Zadaniem stworzonej aplikacji jest analiza tekstów literackich, która
      polega na wykryciu bytów, wyznaczeniu ich częstości występowania oraz
      powiązań pomiędzy nimi. Aplikacja umożliwia wgranie tekstu, którego wyniki
      analizy zostają zaprezentowane w postaci grafu. Zaimplementowane funkcje
      umożliwiają przeglądanie oraz edycję prezentowanego grafu. Użytkownik
      posiada możliwość zapisu do pliku edytowanego grafu. Dodatkowo aplikacja
      przechowuje w bazie danych wcześniej przeanalizowane grafy, aby użytkownik
      nie musiał zlecać zadania analizy tego samego tekstu dwa razy.<br /><br />
    </h3>
    <table style="width:100%">
      <tr>
        <th>
          <img src="@/assets/images/upload-tekstu.png" />
        </th>
        <th style="text-align: justify">
          Wczytywanie tekstu możliwe jest po wpisaniu go ręcznie lub poprzez
          wczytanie pliku. <br />
          Program obsługuje pliki tekstowe w następujących formatach: *.txt,
          *.pdf.<br />
          Plik *.pdf musi zawierać tekst, czytanie tekstu z obrazów (OCR) nie
          jest wspierane.<br />
          Po załadowaniu tekstu możliwa jest jego edycja.<br />
        </th>
      </tr>
      <tr>
        <th style="text-align: justify">
          Dane zwracane z przeanalizowanego tekstu zwracają wagi połączeń
          pomiędzy bytami oraz liczbę wystąpień postaci.<br />
          Użytkownik posiada możliwość ręcznego złączenia dwóch bytów w jeden.
          Przed złączeniem, wybrane byty zostają podświetlone.
          <br />
          Funkcjonalność ta jest przydatna w przypadku gdy jeden byt zostanie
          błędnie rozróżniony jako dwa osobne. <br />
          Wszelkie zmiany dokonane przez użytkownika mogą zostać przywrócone
          przyciskiem Przywróć zmiany.<br />
        </th>
        <th><img src="@/assets/images/merge.png" /></th>
      </tr>
    </table>
  </div>
</template>

<script>
export default {};
</script>

<style scoped>
img {
  width: 100%;
  height: 50%;
}
</style>
