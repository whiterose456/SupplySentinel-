type Props = {
  title: string;
  value: string;
};

export function LiveMetrics({ title, value }: Props) {
  return (
    <div style={{ border: '1px solid #e2e8f0', borderRadius: 12, padding: 12, background: '#f8fafc' }}>
      <div style={{ fontSize: 12, color: '#64748b', textTransform: 'uppercase' }}>{title}</div>
      <div style={{ fontSize: 20, fontWeight: 700, marginTop: 4 }}>{value}</div>
    </div>
  );
}
