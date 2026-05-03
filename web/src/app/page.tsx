import { WelcomeDishCard } from "@/components/welcome-dish-card";
import styles from "./page.module.css";

export default function Home() {
  return (
    <main className={styles.main}>
      <h1 className={styles.title}>chefwho.codes</h1>
      <p className={styles.subtitle}>
        Development environment is live. Generate your first welcome dish.
      </p>
      <WelcomeDishCard />
    </main>
  );
}
