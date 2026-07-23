export function SkeletonLoader() {
  return (
    <div style={{ display: 'grid', gap: 8 }}>
      <div style={{ height: 12, width: '70%', background: '#e2e8f0', borderRadius: 999 }} />
      <div style={{ height: 12, width: '90%', background: '#f1f5f9', borderRadius: 999 }} />
      <div style={{ height: 12, width: '60%', background: '#e2e8f0', borderRadius: 999 }} />
    </div>
  );
}
