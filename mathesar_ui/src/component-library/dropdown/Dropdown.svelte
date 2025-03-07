<script lang="ts">
  import { faAngleDown } from '@fortawesome/free-solid-svg-icons';
  import type { Placement } from '@popperjs/core/lib/enums';
  import {
    createEventDispatcher,
    getContext,
    onDestroy,
    setContext,
    tick,
  } from 'svelte';
  import { derived } from 'svelte/store';
  import type { Appearance, Size } from '@mathesar-component-library-dir/types';
  import Button from '@mathesar-component-library-dir/button/Button.svelte';
  import Icon from '@mathesar-component-library-dir/icon/Icon.svelte';
  import portal from '@mathesar-component-library-dir/common/actions/portal';
  import popper from '@mathesar-component-library-dir/common/actions/popper';
  import clickOffBounds from '@mathesar-component-library-dir/common/actions/clickOffBounds';
  import { AccompanyingElements } from './AccompanyingElements';

  const dispatch = createEventDispatcher();

  export let triggerClass = '';
  export let triggerAppearance: Appearance = 'default';
  export let contentClass = '';
  export let isOpen = false;
  export let closeOnInnerClick = false;
  export let ariaLabel: string | undefined = undefined;
  export let ariaControls: string | undefined = undefined;
  export let placement: Placement = 'bottom-start';
  export let showArrow = true;
  export let size: Size = 'medium';

  let triggerElement: HTMLElement | undefined;
  let contentElement: HTMLElement | undefined;

  const parentAccompanyingElements = getContext<
    AccompanyingElements | undefined
  >('dropdownAccompanyingElements');
  async function setThisContentToAccompanyParent() {
    if (!contentElement) {
      await tick();
    }
    if (!contentElement) {
      return;
    }
    parentAccompanyingElements?.add(contentElement);
  }
  async function unsetThisContentToAccompanyParent() {
    if (!contentElement) {
      await tick();
    }
    if (!contentElement) {
      return;
    }
    parentAccompanyingElements?.delete(contentElement);
  }
  onDestroy(unsetThisContentToAccompanyParent);

  const accompanyingElements = new AccompanyingElements(
    parentAccompanyingElements,
  );
  setContext('dropdownAccompanyingElements', accompanyingElements);

  const clickOffBoundsReferences = derived(
    accompanyingElements,
    (_accompanyingElements) => [triggerElement, ..._accompanyingElements],
  );

  function calculateTriggerClass(
    _triggerClass: string,
    _showArrow: boolean,
  ): string {
    const classes = ['dropdown', 'trigger'];
    if (_triggerClass) {
      classes.push(_triggerClass);
    }
    if (!_showArrow) {
      classes.push('no-arrow');
    }
    return classes.join(' ');
  }

  $: tgClasses = calculateTriggerClass(triggerClass, showArrow);

  function toggle() {
    isOpen = !isOpen;
  }

  function close() {
    isOpen = false;
  }

  function watchIsOpen(_isOpen: boolean) {
    if (_isOpen) {
      dispatch('open');
      void setThisContentToAccompanyParent();
    } else {
      dispatch('close');
      void unsetThisContentToAccompanyParent();
    }
  }
  $: watchIsOpen(isOpen);

  function checkAndCloseOnInnerClick() {
    if (closeOnInnerClick) {
      close();
    }
  }
</script>

<Button
  bind:element={triggerElement}
  appearance={triggerAppearance}
  class={tgClasses}
  on:click={toggle}
  aria-controls={ariaControls}
  aria-haspopup="listbox"
  aria-label={ariaLabel}
  {size}
  on:keydown
  {...$$restProps}
>
  <span class="label">
    <slot name="trigger" />
  </span>
  {#if showArrow}
    <span class="arrow">
      <Icon data={faAngleDown} />
    </span>
  {/if}
</Button>

{#if isOpen}
  <div
    class={['dropdown content', contentClass].join(' ')}
    bind:this={contentElement}
    use:portal
    use:popper={{
      /* @ts-ignore: https://github.com/centerofci/mathesar/issues/1055 */
      reference: triggerElement,
      options: { placement },
    }}
    use:clickOffBounds={{
      callback: close,
      /* @ts-ignore: https://github.com/centerofci/mathesar/issues/1055 */
      references: clickOffBoundsReferences,
    }}
    on:click={checkAndCloseOnInnerClick}
  >
    <slot name="content" />
  </div>
{/if}
