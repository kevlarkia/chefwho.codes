"use client";

import { useMemo, useState } from "react";
import styles from "./welcome-dish-card.module.css";
import { pickWelcomeDish } from "@/lib/welcome-dish";

export function WelcomeDishCard() {
  const [seed, setSeed] = useState(0);
  const [activations, setActivations] = useState(0);

  const dish = useMemo(() => pickWelcomeDish(seed), [seed]);

  return (
    <section className={styles.card}>
      <h2 className={styles.heading}>Hello world task</h2>
      <p>
        Click <strong>Generate welcome dish</strong> to run the first core app
        action.
      </p>
      <p className={styles.output} data-testid="welcome-dish-output">
        {dish}
      </p>
      <button
        className={styles.button}
        type="button"
        onClick={() => {
          setActivations((count) => count + 1);
          setSeed((current) => current + 1);
        }}
      >
        Generate welcome dish
      </button>
      <p className={styles.meta} data-testid="hello-world-count">
        Hello-world action count: {activations}
      </p>
    </section>
  );
}
