type Props = {
  scenario: string;
};

export function ScenarioBuilder({ scenario }: Props) {
  return (
    <div style={{ border: '1px solid #dbeafe', borderRadius: 16, padding: 16, background: '#eff6ff' }}>
      <h2 style={{ marginTop: 0 }}>Scenario Builder</h2>
      <p style={{ marginBottom: 0 }}>Current scenario: <strong>{scenario}</strong></p>
    </div>
  );
}
