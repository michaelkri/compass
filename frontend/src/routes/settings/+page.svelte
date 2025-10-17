<script lang="ts">
    import { onMount } from "svelte";

    const url = "http://localhost:8000/api/search_terms/";

    let newTerm: any = $state("");

    let searchTerms: any[] = $state([]);

    onMount(async () => {
        try {
            const response = await fetch(url);
            const data = await response.json();
            searchTerms = data.terms;
        }
        catch (error) {
            console.error(error);
        }
    });

    async function createSearchTerm() {
        if (newTerm.length > 0) {
            try {
                const response = await fetch(
                    url,
                    {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                        },
                        body: JSON.stringify({ term: newTerm }),
                    },
                );

                if (response.status === 201) {
                    const newItem = await response.json();                    
                    searchTerms.push(newItem);
                    newTerm = "";
                }
                else {
                    console.log(response.status);
                }

            } catch (error) {
                console.error(error);
            }
        }
    }

    async function deleteTerm(termId: any) {
        try {
            const response = await fetch(
                url + termId,
                {
                    method: "DELETE"
                }
            );

            if (response.status === 204) {
                searchTerms = searchTerms.filter(term => term.id != termId);
            }
            else {
                console.log(response.status);
            }
        }
        catch (error) {
            console.error(error);
        }
    }
</script>

<section class="text-gray-900 dark:text-white">
    <div class="py-8 px-4 mx-auto max-w-2xl lg:py-16">
        <div class="mb-4">
            <h1 class="text-2xl font-bold">Settings</h1>
        </div>

        <div class="border-b border-border pb-4">
            <h2 class="text-xl font-bold">Job Titles</h2>
            <span class="text-gray-700 dark:text-gray-400"
                >Add, view and manage job titles to search for.</span
            >

            <div class="mt-4 flex items-center gap-3">
                <input
                    type="text"
                    name="term"
                    id="term"
                    placeholder="Enter a new search term..."
                    class="flex-grow bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500"
                    bind:value={newTerm}
                />
                <button
                    class="p-3 text-sm font-medium text-center text-white bg-blue-500 rounded-lg cursor-pointer hover:bg-blue-800"
                    onclick={createSearchTerm}>Add Term</button
                >
            </div>

            <div class="mt-4">
                {#each searchTerms as term (term.id)}
                    <div
                        class="p-3 flex items-center gap-3 rounded-lg border-1 border-gray-200 mb-2"
                    >
                        <h4 class="flex-grow">{term.term}</h4>
                        <button
                            onclick={() => deleteTerm(term.id)}
                            class="cursor-pointer underline text-red-700"
                            >Delete</button
                        >
                    </div>
                {/each}
            </div>
        </div>
    </div>
</section>
