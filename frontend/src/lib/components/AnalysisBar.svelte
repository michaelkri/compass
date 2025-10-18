<script lang="ts">
    import AnalysisInsight from "./AnalysisInsight.svelte";
    import AnalysisPoint from "./AnalysisPoint.svelte";
    import AnalysisScore from "./AnalysisScore.svelte";
    import AnalysisSection from "./AnalysisSection.svelte";

    let { selectedJob } = $props();

    let isGenerating = $state(false);

    async function generateAnalysis(job: any) {
        isGenerating = true;

        try {
            const response = await fetch("http://localhost:8000/api/analysis/" + job.id);
            
            if (response.status === 200) {
                const data = await response.json();
                return data;
            }
            else {
                console.log(response.status);
            }
        }
        catch (error) {
            console.error(error);
        }
        finally {
            isGenerating = false;
        }
    }
</script>

{#if selectedJob == null}
    <p>Select a job to view AI analysis</p>
{:else if selectedJob.analysis == null}
    <div class="flex h-48 w-full items-center justify-center">
        <button
            class="cursor-pointer group relative inline-flex items-center justify-center rounded-lg border border-slate-900/10 bg-white/40 px-8 py-3 font-medium text-slate-800 backdrop-blur-md transition-all duration-300 hover:bg-gradient-to-r from-blue-600 to-purple-600 hover:text-white dark:text-white dark:bg-gray-800 disabled:cursor-not-allowed disabled:bg-gradient-to-r disabled:text-white animate-gradient"
            onclick={async () => {
                const analysis = await generateAnalysis(selectedJob);
                selectedJob = { ...selectedJob, analysis };
            }}
            disabled={isGenerating}
        >
            <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke-width="2"
                stroke="currentColor"
                class="mr-3 h-6 w-6"
            >
                <path
                    d="m21.64 3.64-1.28-1.28a1.21 1.21 0 0 0-1.72 0L2.36 18.64a1.21 1.21 0 0 0 0 1.72l1.28 1.28a1.2 1.2 0 0 0 1.72 0L21.64 5.36a1.2 1.2 0 0 0 0-1.72"
                /><path d="m14 7 3 3" /><path d="M5 6v4" /><path
                    d="M19 14v4"
                /><path d="M10 2v2" /><path d="M7 8H3" /><path
                    d="M21 16h-4"
                /><path d="M11 3H9" />
            </svg>

            <span>
                {#if !isGenerating}
                    Generate Analysis
                {:else}
                    Generating Analysis...
                {/if}
            </span>
        </button>
    </div>
{:else}
    <AnalysisScore
        score={selectedJob.analysis.candidate_fit_score}
        summary={selectedJob.analysis.application_summary}
    />

    <AnalysisSection title="Top Strengths">
        {#each selectedJob.analysis.top_strengths as strength}
            <AnalysisPoint
                point={strength}
                style={"bg-green-50 border-green-400 text-green-900"}
            />
        {/each}
    </AnalysisSection>

    <AnalysisSection title="Key Gaps">
        {#each selectedJob.analysis.key_gaps as gap}
            <AnalysisPoint
                point={gap}
                style={"bg-red-50 border-red-400 text-red-900"}
            />
        {/each}
    </AnalysisSection>

    <AnalysisSection title="Possible Interview Questions">
        {#each selectedJob.analysis.possible_questions as question}
            <AnalysisPoint
                point={question}
                style={"bg-yellow-50 border-yellow-400 text-yellow-900"}
            />
        {/each}
    </AnalysisSection>

    <AnalysisSection title="Insights">
        {#each selectedJob.analysis.insights_list as insight}
            <AnalysisInsight {...insight} />
        {/each}
    </AnalysisSection>
{/if}

<style>
    .animate-gradient {
        background-size: 300%;
        animation: animatedgradient 6s ease infinite alternate;
    }

    @keyframes animatedgradient {
        0% {
            background-position: 0% 50%;
        }
        50% {
            background-position: 100% 50%;
        }
        100% {
            background-position: 0% 50%;
        }
    }
</style>