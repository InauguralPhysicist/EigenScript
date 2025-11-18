"""
LRVM (Lightlike-Relational Vector Model) implementation.

This module defines the geometric vector representation used in EigenScript's
semantic model. Every value and expression exists as a vector in LRVM space.
"""

import numpy as np
from typing import Union, List


class LRVMVector:
    """
    Represents a vector in the Lightlike-Relational Vector Model (LRVM) space.

    In EigenScript's geometric model, every value, expression, and operation
    exists as a point in this high-dimensional semantic space. The metric tensor
    defines the geometric properties of this space.

    Attributes:
        coords: NumPy array of coordinates
        dimension: Dimensionality of the vector

    Example:
        >>> v = LRVMVector([1.0, 0.0, -1.0])
        >>> v.dimension
        3
        >>> v.coords
        array([ 1.,  0., -1.])
    """

    def __init__(self, coordinates: Union[np.ndarray, List[float]]):
        """
        Initialize an LRVM vector.

        Args:
            coordinates: Vector coordinates (array-like)
        """
        if isinstance(coordinates, list):
            self.coords = np.array(coordinates, dtype=np.float64)
        else:
            self.coords = np.array(coordinates, dtype=np.float64)

        self.dimension = len(self.coords)

    def norm(self, metric: np.ndarray) -> float:
        """
        Compute the geometric norm of this vector.

        Uses the metric tensor to compute ||v||² = v^T g v

        Args:
            metric: Metric tensor g

        Returns:
            Norm squared value (can be positive, negative, or zero)

        Example:
            >>> v = LRVMVector([1.0, 0.0, 0.0])
            >>> g = np.eye(3)
            >>> v.norm(g)
            1.0
        """
        return float(self.coords.T @ metric @ self.coords)

    def signature_type(self, metric: np.ndarray, epsilon: float = 1e-10) -> str:
        """
        Determine the geometric type based on norm signature.

        Args:
            metric: Metric tensor g
            epsilon: Threshold for considering norm as zero

        Returns:
            "lightlike" if ||v||² ≈ 0
            "spacelike" if ||v||² > 0
            "timelike" if ||v||² < 0

        Example:
            >>> v = LRVMVector([1.0, 1.0, 0.0])
            >>> g = np.eye(3)
            >>> v.signature_type(g)
            'spacelike'
        """
        n = self.norm(metric)

        if abs(n) < epsilon:
            return "lightlike"
        elif n > 0:
            return "spacelike"
        else:
            return "timelike"

    def add(self, other: "LRVMVector") -> "LRVMVector":
        """
        Vector addition.

        Args:
            other: Another LRVM vector

        Returns:
            New vector representing the sum

        Raises:
            ValueError: If dimensions don't match
        """
        if self.dimension != other.dimension:
            raise ValueError(
                f"Dimension mismatch: {self.dimension} vs {other.dimension}"
            )

        return LRVMVector(self.coords + other.coords)

    def subtract(self, other: "LRVMVector") -> "LRVMVector":
        """
        Vector subtraction.

        Args:
            other: Another LRVM vector

        Returns:
            New vector representing the difference

        Raises:
            ValueError: If dimensions don't match
        """
        if self.dimension != other.dimension:
            raise ValueError(
                f"Dimension mismatch: {self.dimension} vs {other.dimension}"
            )

        return LRVMVector(self.coords - other.coords)

    def scale(self, scalar: float) -> "LRVMVector":
        """
        Scalar multiplication.

        Args:
            scalar: Scaling factor

        Returns:
            New scaled vector
        """
        return LRVMVector(scalar * self.coords)

    def dot(self, other: "LRVMVector") -> float:
        """
        Standard Euclidean dot product (not using metric).

        For metric-aware contraction, use MetricTensor.contract()

        Args:
            other: Another LRVM vector

        Returns:
            Scalar dot product

        Raises:
            ValueError: If dimensions don't match
        """
        if self.dimension != other.dimension:
            raise ValueError(
                f"Dimension mismatch: {self.dimension} vs {other.dimension}"
            )

        return float(np.dot(self.coords, other.coords))

    def distance(self, other: "LRVMVector", metric: np.ndarray) -> float:
        """
        Compute geometric distance to another vector.

        Uses metric: d(v1, v2) = sqrt(||(v1 - v2)||²)

        Args:
            other: Another LRVM vector
            metric: Metric tensor g

        Returns:
            Distance (absolute value of norm for proper distance)
        """
        diff = self.subtract(other)
        norm_squared = diff.norm(metric)
        return float(np.sqrt(abs(norm_squared)))

    def __repr__(self) -> str:
        """String representation."""
        return f"LRVMVector({self.coords.tolist()[:5]}{'...' if self.dimension > 5 else ''}, dim={self.dimension})"

    def __eq__(self, other: object) -> bool:
        """Equality comparison."""
        if not isinstance(other, LRVMVector):
            return False
        return np.allclose(self.coords, other.coords)

    def __hash__(self) -> int:
        """Hash for use in sets/dicts."""
        return hash(tuple(self.coords.tolist()))


class LRVMSpace:
    """
    Represents the entire LRVM semantic space.

    This class manages the embedding of values into LRVM vectors
    and provides utilities for working in the space.
    """

    def __init__(self, dimension: int = 768):
        """
        Initialize LRVM space with given dimensionality.

        Args:
            dimension: Dimensionality of the vector space (default: 768, BERT-like)
        """
        self.dimension = dimension

    def zero_vector(self) -> LRVMVector:
        """
        Create a zero vector in this space.

        Returns:
            Zero vector
        """
        return LRVMVector(np.zeros(self.dimension))

    def random_vector(self, scale: float = 1.0) -> LRVMVector:
        """
        Create a random vector (for testing/initialization).

        Args:
            scale: Scaling factor for random values

        Returns:
            Random LRVM vector
        """
        coords = np.random.randn(self.dimension) * scale
        return LRVMVector(coords)

    def embed_scalar(self, value: float) -> LRVMVector:
        """
        Embed a scalar number into LRVM space.

        This is a simple embedding strategy - can be made more sophisticated.

        Args:
            value: Scalar number to embed

        Returns:
            LRVM vector representation

        Example:
            >>> space = LRVMSpace(dimension=3)
            >>> v = space.embed_scalar(5.0)
        """
        # TODO: Implement proper scalar embedding
        # For now, simple strategy: put value in first coordinate
        coords = np.zeros(self.dimension)
        coords[0] = value
        return LRVMVector(coords)

    def embed_string(self, text: str) -> LRVMVector:
        """
        Embed a string into LRVM space using semantic embedding.

        This should use a pretrained model (like BERT, GPT embeddings, etc.)
        but for now we'll use a simple hash-based approach.

        Args:
            text: String to embed

        Returns:
            LRVM vector representation

        Example:
            >>> space = LRVMSpace(dimension=768)
            >>> v = space.embed_string("hello")
        """
        # TODO: Implement proper string embedding
        # Should use transformer-based embeddings
        # For now, simple hash-based placeholder
        coords = np.zeros(self.dimension)
        hash_val = hash(text)

        # Distribute hash across dimensions
        for i in range(min(10, self.dimension)):
            coords[i] = ((hash_val >> (i * 6)) & 0x3F) / 64.0

        return LRVMVector(coords)
