<template>
    <v-layout justify-center>
        <vue-title title="O projektu"></vue-title>

        <v-flex md11>
            <v-card>
                <v-card-title primary-title>
                    <h1>O projektu</h1>
                </v-card-title>
                <v-card-text>
                    <p>
                        Aplikace slouží pro zobrazování a doporučování denních menu.
                    </p>

                    <h2>Technické detaily</h2>

                    <h3>Zdroj dat</h3>

                    <p>
                        Jako zdroj dat denních menu se používají stránky restaurací, veřejně dostupné API služby
                        Zomato.com a
                        informace o denních menu získaných z portálu
                        <a href="https://menupraha.cz" target="_blank">MenuPraha.cz</a>.
                    </p>


                    <h3>Klasifikace dat</h3>

                    <p>
                        Pro klasifikaci jednotlivých denních menu jsou využívána jednak data z vybraných restaurací pro
                        klasifikaci
                        podle kuchyně (mexická, italská, vietnamská, ...) a jednak ze stránek poskytujících recepty.
                        Aktálně
                        aplikace používá data ze serverů <a href="https://recepty.cz" target="_blank">recepty.cz</a> a
                        <a href="https://toprecepty.cz">TopRecepty.cz</a>.
                    </p>

                    <h2>Prohlášení</h2>
                    <p>
                        Aplikace je provozována bez jakékoliv záruky, zcela zdarma a čistě pro osobní použití.
                    </p>
                </v-card-text>
            </v-card>
        </v-flex>
    </v-layout>
</template>

<script>
    export default {}
</script>
