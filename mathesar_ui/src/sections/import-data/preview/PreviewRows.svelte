<script lang="ts">
  import { get } from 'svelte/store';
  import { onMount } from 'svelte';
  import { postAPI, States } from '@mathesar/utils/api';
  import { setInFileStore } from '@mathesar/stores/fileImports';
  import type { FileImport, PreviewRow } from '@mathesar/stores/fileImports';
  import CellValue from '@mathesar/components/CellValue.svelte';
  import type { CancellablePromise } from '@mathesar-component-library';

  interface Response {
    records: PreviewRow[];
  }

  export let fileImportStore: FileImport;
  let previewPromise: CancellablePromise<Response>;

  async function getRows() {
    previewPromise?.cancel();
    try {
      const fileImportData = get(fileImportStore);
      const columnInfo = fileImportData.previewColumns?.map((column) => ({
        name: column.name,
        type: column.type,
      }));
      setInFileStore(fileImportStore, {
        previewRowsLoadStatus: States.Loading,
        error: undefined,
      });
      previewPromise = postAPI<Response>(
        // eslint-disable-next-line @typescript-eslint/restrict-template-expressions
        `/tables/${fileImportData.previewId}/previews/`,
        {
          columns: columnInfo,
        },
      );
      const result = await previewPromise;
      setInFileStore(fileImportStore, {
        previewRowsLoadStatus: States.Done,
        previewRows: result.records || [],
      });
    } catch (err) {
      setInFileStore(fileImportStore, {
        previewRowsLoadStatus: States.Error,
        error: (err as Error).message,
        previewRows: [],
      });
    }
  }

  onMount(() => {
    void getRows();

    return () => {
      previewPromise?.cancel();
    };
  });
</script>

{#each $fileImportStore.previewRows || [] as row (row)}
  <tr>
    {#each $fileImportStore.previewColumns || [] as column (column.name)}
      <td>
        <CellValue value={row[column.name]} />
      </td>
    {/each}
  </tr>
{/each}
