<script lang="ts">
  import { getContext } from 'svelte';
  import {
    Pagination as PaginationComponent,
    Select,
  } from '@mathesar-component-library';
  import { States } from '@mathesar/utils/api';
  import type { TabularDataStore } from '@mathesar/stores/table-data/types';
  import { Pagination } from '@mathesar/stores/table-data';

  const tabularData = getContext<TabularDataStore>('tabularData');

  $: ({ recordsData, meta } = $tabularData);
  $: ({ selectedRecords, pagination } = meta);
  $: ({ size: pageSize, page, offset } = $pagination);
  $: ({ totalCount, state, newRecords } = recordsData);
  $: recordState = $state;
  $: selectedPageSize = { id: pageSize, label: pageSize };

  const pageSizeOpts = [
    { id: 100, label: '100' },
    { id: 200, label: '200' },
    { id: 500, label: '500' },
  ];

  let pageCount: number;
  $: max = Math.min($totalCount ?? 0, offset + pageSize);

  function handlePageChange(event: {
    detail: {
      currentPage: number;
    };
  }) {
    pagination.update(
      (p) => new Pagination({ ...p, page: event.detail.currentPage }),
    );
  }

  function setPageSize(
    event: CustomEvent<{ value: { id: number; label: string } }>,
  ) {
    const newPageSize = event.detail.value.id;
    if (pageSize !== newPageSize) {
      $pagination = new Pagination({ page: 1, size: newPageSize });
    }
  }
</script>

<div class="status-pane">
  <div class="record-count">
    {#if $selectedRecords?.size > 0}
      {$selectedRecords.size} record{$selectedRecords.size > 1 ? 's' : ''} selected
      of {$totalCount}
    {:else if pageCount > 0 && $totalCount}
      Showing {offset + 1} to {max}
      {#if $newRecords.length > 0}
        (+ {$newRecords.length} new record{$newRecords.length > 1 ? 's' : ''})
      {/if}
      of {$totalCount} records
    {:else if recordState !== States.Loading}
      No records found
    {/if}
  </div>

  <div class="pagination-group">
    {#if $totalCount}
      <PaginationComponent
        total={$totalCount}
        {pageSize}
        bind:pageCount
        currentPage={page}
        on:change={handlePageChange}
      />
      <Select
        options={pageSizeOpts}
        value={selectedPageSize}
        on:change={setPageSize}
      />
    {/if}
  </div>
</div>

<style global lang="scss">
  @import 'StatusPane.scss';
</style>
